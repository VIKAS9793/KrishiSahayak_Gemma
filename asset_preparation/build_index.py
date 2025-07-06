# ==============================================================================
# RAG System Performance Optimizations
# ==============================================================================

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from tqdm import tqdm
import warnings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OptimizedRAGIndexer:
    """
    Optimized RAG indexer with performance improvements and error handling.
    """
    
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        batch_size: int = 32,
        use_gpu: bool = False
    ):
        self.model_name = model_name
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.batch_size = batch_size
        self.use_gpu = use_gpu
        self.embedding_model = None
        self.index = None
        self.texts = []
        
        # Optimize Windows environment
        self._optimize_windows_environment()
    
    def _optimize_windows_environment(self):
        """Optimize environment for Windows systems."""
        # Disable HuggingFace symlink warnings
        os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'
        
        # Set cache directory to avoid permission issues
        cache_dir = Path.home() / ".cache" / "huggingface"
        cache_dir.mkdir(parents=True, exist_ok=True)
        os.environ['HF_HOME'] = str(cache_dir)
        
        # Optimize for CPU performance
        os.environ['OMP_NUM_THREADS'] = str(os.cpu_count())
        os.environ['MKL_NUM_THREADS'] = str(os.cpu_count())
    
    def load_embedding_model(self):
        """Load embedding model with optimizations."""
        logger.info(f"Loading embedding model: '{self.model_name}'")
        
        try:
            device = 'cuda' if self.use_gpu else 'cpu'
            self.embedding_model = SentenceTransformer(
                self.model_name,
                device=device,
                trust_remote_code=True
            )
            
            # Optimize model for inference
            self.embedding_model.eval()
            if hasattr(self.embedding_model, 'half') and self.use_gpu:
                self.embedding_model.half()  # Use FP16 for GPU
            
            logger.info(f"✅ Embedding model loaded on {device}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load embedding model: {e}")
            raise
    
    def create_optimized_chunks(self, text: str) -> List[str]:
        """Create optimized text chunks with better boundary detection."""
        if not text or len(text.strip()) < 10:
            return []
        
        # Split by sentences first
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Check if adding this sentence exceeds chunk size
            if len(current_chunk) + len(sentence) + 2 > self.chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    # Start new chunk with overlap
                    overlap_words = current_chunk.split()[-self.chunk_overlap:]
                    current_chunk = " ".join(overlap_words) + " " + sentence
                else:
                    current_chunk = sentence
            else:
                current_chunk = current_chunk + ". " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def process_knowledge_base(self, csv_path: str) -> List[str]:
        """Process knowledge base with improved chunking."""
        logger.info(f"Loading raw data from: {csv_path}")
        
        try:
            df = pd.read_csv(csv_path)
            all_chunks = []
            
            # Process each row
            for idx, row in tqdm(df.iterrows(), total=len(df), desc="Processing documents"):
                # Combine all text fields
                text_fields = []
                for col in df.columns:
                    if pd.notna(row[col]) and isinstance(row[col], str):
                        text_fields.append(str(row[col]).strip())
                
                combined_text = " ".join(text_fields)
                
                # Create chunks
                chunks = self.create_optimized_chunks(combined_text)
                
                # Add metadata to chunks
                for chunk in chunks:
                    chunk_with_meta = f"[Source: Row {idx+1}] {chunk}"
                    all_chunks.append(chunk_with_meta)
            
            logger.info(f"✅ Successfully created {len(all_chunks)} text chunks")
            return all_chunks
            
        except Exception as e:
            logger.error(f"❌ Failed to process knowledge base: {e}")
            raise
    
    def generate_embeddings_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings in batches for better performance."""
        if not self.embedding_model:
            raise ValueError("Embedding model not loaded")
        
        logger.info(f"Generating embeddings for {len(texts)} texts")
        
        try:
            # Process in batches to avoid memory issues
            all_embeddings = []
            
            for i in tqdm(range(0, len(texts), self.batch_size), desc="Generating embeddings"):
                batch_texts = texts[i:i + self.batch_size]
                
                # Generate embeddings for batch
                batch_embeddings = self.embedding_model.encode(
                    batch_texts,
                    batch_size=self.batch_size,
                    show_progress_bar=False,
                    convert_to_numpy=True,
                    normalize_embeddings=True  # Normalize for better similarity search
                )
                
                all_embeddings.append(batch_embeddings)
            
            # Concatenate all embeddings
            embeddings = np.vstack(all_embeddings)
            
            logger.info(f"✅ Generated {len(embeddings)} embeddings of dimension {embeddings.shape[1]}")
            return embeddings
            
        except Exception as e:
            logger.error(f"❌ Failed to generate embeddings: {e}")
            raise
    
    def build_faiss_index(self, embeddings: np.ndarray) -> faiss.Index:
        """Build optimized FAISS index."""
        logger.info("Building FAISS index")
        
        try:
            dimension = embeddings.shape[1]
            
            # Choose index type based on data size
            if len(embeddings) < 1000:
                # Use flat index for small datasets
                index = faiss.IndexFlatIP(dimension)  # Inner product for normalized vectors
            else:
                # Use IVF index for larger datasets
                nlist = min(100, int(np.sqrt(len(embeddings))))
                quantizer = faiss.IndexFlatIP(dimension)
                index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
                
                # Train the index
                index.train(embeddings.astype(np.float32))
            
            # Add embeddings to index
            index.add(embeddings.astype(np.float32))
            
            logger.info(f"✅ FAISS index built with {index.ntotal} vectors")
            return index
            
        except Exception as e:
            logger.error(f"❌ Failed to build FAISS index: {e}")
            raise
    
    def save_index_and_texts(self, index: faiss.Index, texts: List[str], 
                           index_path: str, texts_path: str):
        """Save FAISS index and texts with error handling."""
        try:
            # Save FAISS index
            faiss.write_index(index, index_path)
            logger.info(f"✅ FAISS index saved to: {index_path}")
            
            # Save texts
            with open(texts_path, 'wb') as f:
                pickle.dump(texts, f, protocol=pickle.HIGHEST_PROTOCOL)
            logger.info(f"✅ Text data saved to: {texts_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save index/texts: {e}")
            raise
    
    def build_complete_index(self, csv_path: str, output_dir: str):
        """Build complete RAG index with all optimizations."""
        logger.info("--- Starting Optimized Knowledge Base Indexing ---")
        
        try:
            # Ensure output directory exists
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Load embedding model
            self.load_embedding_model()
            
            # Process knowledge base
            self.texts = self.process_knowledge_base(csv_path)
            
            # Generate embeddings
            embeddings = self.generate_embeddings_batch(self.texts)
            
            # Build FAISS index
            self.index = self.build_faiss_index(embeddings)
            
            # Save index and texts
            index_path = Path(output_dir) / "knowledge_base.faiss"
            texts_path = Path(output_dir) / "knowledge_base_text.pkl"
            
            self.save_index_and_texts(self.index, self.texts, 
                                    str(index_path), str(texts_path))
            
            # Performance summary
            self._print_performance_summary()
            
            logger.info("--- ✅ Optimized Knowledge Base Indexing Complete ---")
            
        except Exception as e:
            logger.error(f"❌ Indexing failed: {e}")
            raise
    
    def _print_performance_summary(self):
        """Print performance summary."""
        if self.texts and self.index:
            print("\n" + "="*60)
            print("📊 PERFORMANCE SUMMARY")
            print("="*60)
            print(f"📄 Total text chunks: {len(self.texts)}")
            print(f"🔍 FAISS index size: {self.index.ntotal} vectors")
            print(f"📐 Embedding dimension: {self.index.d}")
            print(f"🎯 Model: {self.model_name}")
            print(f"⚡ Batch size: {self.batch_size}")
            print("="*60)

# ==============================================================================
# Usage Example
# ==============================================================================

def main():
    """Main function to run optimized indexing."""
    
    # Configuration
    config = {
        "model_name": "all-MiniLM-L6-v2",
        "chunk_size": 512,
        "chunk_overlap": 50,
        "batch_size": 32,
        "use_gpu": False  # Set to True if you have CUDA GPU
    }
    
    # Paths
    csv_path = "data/processed/knowledge_base.csv"
    output_dir = "data/processed"
    
    # Create optimized indexer
    indexer = OptimizedRAGIndexer(**config)
    
    # Build index
    indexer.build_complete_index(csv_path, output_dir)

if __name__ == "__main__":
    main()
