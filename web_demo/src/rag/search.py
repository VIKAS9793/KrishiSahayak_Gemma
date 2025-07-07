# --- src/rag/search.py ---

import faiss
import numpy as np
import os
import pickle
from sentence_transformers import SentenceTransformer

# --- Configuration ---
# This must match the model used in build_index.py
EMBEDDING_MODEL_ID = 'all-MiniLM-L6-v2'
ARCHIVE_DIR = "../../data/_archive"
INDEX_FILE_PATH = os.path.join(ARCHIVE_DIR, "knowledge_base_v0_generic_46-class.faiss")
TEXT_DATA_PATH = os.path.join(ARCHIVE_DIR, "knowledge_base_v0_generic_46-class_text.pkl")

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

def search_knowledge_base(query: str, top_k: int = 3) -> list[str]:
    """
    Searches the knowledge base for text chunks relevant to the query.

    Args:
        query (str): The user's query text.
        top_k (int): The number of top results to return.

    Returns:
        list[str]: A list of the most relevant text chunks from the knowledge base.
                   Returns an empty list if an error occurs.
    """
    try:
        # Ensure all dependencies are loaded
        load_search_dependencies()

        print(f"\nSearching for top {top_k} results for query: '{query}'")
        
        # 1. Encode the query into a vector
        query_embedding = embedding_model.encode([query], convert_to_tensor=False)
        query_embedding = np.array(query_embedding, dtype=np.float32)

        # 2. Search the FAISS index
        # D: distances, I: indices
        distances, indices = index.search(query_embedding, top_k)

        # 3. Retrieve the corresponding text chunks
        results = [text_data[i] for i in indices[0]]
        
        print("✅ Search complete.")
        return results

    except FileNotFoundError as e:
        print(e)
        return []
    except Exception as e:
        print(f"❌ An unexpected error occurred during search: {e}")
        return []

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

