# --- src/rag/search.py ---

import faiss
import numpy as np
import os
import pickle
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sentence_transformers import SentenceTransformer

# Import our utilities
from ..utils.cache_utils import get_cache, set_cache, rate_limit, with_retry
from .monitoring import monitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rag_search.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Configuration ---
# This must match the model used in build_index.py
EMBEDDING_MODEL_ID = 'all-MiniLM-L6-v2'
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data', 'processed')
INDEX_FILE_PATH = os.path.join(DATA_DIR, "knowledge_base_v0_generic_46-class.faiss")
TEXT_DATA_PATH = os.path.join(DATA_DIR, "knowledge_base_v0_generic_46-class_text.pkl")

# Performance monitoring
SEARCH_METRICS = {
    'total_searches': 0,
    'cache_hits': 0,
    'cache_misses': 0,
    'avg_search_time': 0.0,
    'errors': 0,
    'rate_limited_requests': 0
}

# Import time after configuration to avoid circular imports
import time

# --- Global Caching ---
# Load models and data only once to ensure efficiency
embedding_model = None
index = None
text_data = None

def load_search_dependencies():
    """
    Loads all necessary components for searching into memory.
    - FAISS index
    - Text data
    - Embedding model
    """
    global embedding_model, index, text_data

    # --- 1. Load Embedding Model ---
    if embedding_model is None:
        print("Loading embedding model for search...")
        try:
            embedding_model = SentenceTransformer(EMBEDDING_MODEL_ID)
            print("✅ Embedding model loaded.")
        except Exception as e:
            print(f"❌ ERROR: Could not load SentenceTransformer model. {e}")
            raise

    # --- 2. Load FAISS Index ---
    if index is None:
        print(f"Loading FAISS index from: {INDEX_FILE_PATH}")
        if not os.path.exists(INDEX_FILE_PATH):
            raise FileNotFoundError(
                f"FAISS index not found at '{INDEX_FILE_PATH}'. "
                "Please run 'src/rag/build_index.py' first."
            )
        try:
            index = faiss.read_index(INDEX_FILE_PATH)
            print("✅ FAISS index loaded successfully.")
        except Exception as e:
            print(f"❌ ERROR: Could not load FAISS index. {e}")
            raise

    # --- 3. Load Text Data ---
    if text_data is None:
        print(f"Loading text data from: {TEXT_DATA_PATH}")
        if not os.path.exists(TEXT_DATA_PATH):
            raise FileNotFoundError(
                f"Text data not found at '{TEXT_DATA_PATH}'. "
                "Please run 'src/rag/build_index.py' first."
            )
        try:
            with open(TEXT_DATA_PATH, 'rb') as f:
                text_data = pickle.load(f)
            print("✅ Text data loaded successfully.")
        except Exception as e:
            print(f"❌ ERROR: Could not load text data. {e}")
            raise

def search_knowledge_base(query: str, top_k: int = 3, user_id: str = "default") -> list[str]:
    """
    Searches the knowledge base for text chunks relevant to the query.
    Implements caching and rate limiting.

    Args:
        query (str): The user's query text.
        top_k (int, optional): The number of top results to return. Defaults to 3.
        user_id (str, optional): User identifier for rate limiting. Defaults to "default".

    Returns:
        list[str]: A list of the most relevant text chunks from the knowledge base.
                 Returns an empty list if an error occurs, no results found, or rate limited.
    """
    start_time = time.time()
    logger.info(f"Search initiated - User: {user_id}, Query: '{query[:50]}{'...' if len(query) > 50 else ''}'")
    
    # Input validation
    if not query or not query.strip():
        logger.warning("Empty query received")
        return []

    # Check rate limit
    if not rate_limit(user_id):
        logger.warning(f"Rate limit exceeded for user: {user_id}")
        monitor.record_rate_limit()
        return ["Rate limit exceeded. Please try again later."]

    # Check cache first
    cache_start = time.time()
    cached_result = get_cache(query, top_k)
    cache_time = time.time() - cache_start
    
    if cached_result is not None:
        logger.info(f"Cache hit for query: '{query[:50]}...' (took {cache_time:.4f}s)")
        monitor.record_search(cache_hit=True, search_time=cache_time)
        return cached_result
        
    logger.info(f"Cache miss for query: '{query[:50]}...' (check took {cache_time:.4f}s)")
    search_start_time = time.time()

    try:
        # Ensure all dependencies are loaded
        load_search_dependencies()
        
        # Validate we have data to search
        if not text_data or len(text_data) == 0:
            raise ValueError("Knowledge base is empty. Please verify the data files.")
            
        # Adjust top_k if it's larger than our dataset
        top_k = min(top_k, len(text_data))
        
        logger.info(f"Processing search for query: '{query[:50]}...'")
        
        # Perform the search with retry logic
        results = _perform_search(query, top_k)
        
        # Cache the results
        if results:
            set_cache(query, top_k, results)
        
        search_time = time.time() - search_start_time
        total_time = time.time() - start_time
        logger.info(f"Search completed in {search_time:.2f}s (total: {total_time:.2f}s). Found {len(results)} results.")
        
        # Record the search metrics
        monitor.record_search(cache_hit=False, search_time=search_time)
        
        # Log performance metrics periodically
        if monitor.metrics['total_searches'] % 10 == 0:
            metrics = monitor.get_metrics()
            logger.info(
                f"Performance metrics - "
                f"Searches: {metrics['total_searches']}, "
                f"Cache Hit Rate: {metrics.get('cache_hit_rate', 0):.1%}, "
                f"Avg Search Time: {metrics.get('avg_search_time', 0):.3f}s"
            )
            
        return results
        
    except FileNotFoundError as e:
        error_msg = f"Knowledge base files not found: {e}"
        logger.error(error_msg)
        logger.error(f"Please ensure the following files exist:\n- {INDEX_FILE_PATH}\n- {TEXT_DATA_PATH}")
        monitor.record_error("file_not_found")
        return []
        
    except Exception as e:
        error_msg = f"Error in search_knowledge_base: {str(e)}"
        logger.error(error_msg, exc_info=True)
        monitor.record_error("search_error")
        return []

@with_retry(max_retries=3, backoff_factor=0.5)
def _perform_search(query: str, top_k: int) -> List[str]:
    """
    Internal function to perform the actual search with retry logic.
    
    Args:
        query (str): The search query
        top_k (int): Number of results to return
        
    Returns:
        List[str]: List of search results
    """
    try:
        # 1. Encode the query into a vector
        query_embedding = embedding_model.encode([query], convert_to_tensor=False)
        query_embedding = np.array(query_embedding, dtype=np.float32)

        # 2. Search the FAISS index
        # D: distances, I: indices
        distances, indices = index.search(query_embedding, top_k)
        
        # Filter out any invalid indices
        valid_indices = [i for i in indices[0] if 0 <= i < len(text_data)]
        
        if not valid_indices:
            logger.warning("No valid results found in knowledge base")
            return []
            
        # 3. Retrieve the corresponding text chunks with their relevance scores
        results = [
            f"{text_data[i]}\n[Relevance: {1 - distances[0][j]:.2f}]" 
            for j, i in enumerate(valid_indices)
        ]
        
        return results
        
    except Exception as e:
        logger.error(f"Error in _perform_search: {str(e)}", exc_info=True)
        raise  # Let the retry decorator handle it

# --- Self-test block ---
if __name__ == '__main__':
    print("--- Running Knowledge Base Search Self-Test ---")
    
    try:
        # This will load everything
        load_search_dependencies()
        
        # Test with a sample query
        test_query = "my tomato plant has curling leaves"
        search_results = search_knowledge_base(test_query)

        if search_results:
            print("\n--- Search Results ---")
            for i, result in enumerate(search_results):
                print(f"{i+1}. {result}\n")
            print("----------------------")
        else:
            print("\nSearch returned no results. This could be due to an error or an empty index.")

    except Exception as e:
        print(f"\nSelf-test failed: {e}")

