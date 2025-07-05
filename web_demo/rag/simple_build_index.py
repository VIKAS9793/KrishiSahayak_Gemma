# --- src/rag/build_index.py ---
# Version 2: Corrected to use robust, absolute file paths.

import os
# Suppress HuggingFace symlink warnings
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

# --- Configuration ---
EMBEDDING_MODEL_ID = 'all-MiniLM-L6-v2'

# --- Use robust paths relative to this script's location ---
# This ensures the script works regardless of the current working directory.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "knowledge_base.csv")
PROCESSED_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
INDEX_FILE_PATH = os.path.join(PROCESSED_DATA_DIR, "knowledge_base.faiss")
TEXT_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, "knowledge_base_text.pkl")


def create_text_chunks(df: pd.DataFrame) -> list[str]:
    """Processes a DataFrame to create descriptive text chunks for embedding."""
    chunks = []
    for _, row in df.iterrows():
        chunk = (
            f"Disease: {row['disease_name']}. "
            f"Symptoms: {row['symptoms']}. "
            f"Remedy: {row['remedy']}. "
            f"Source: {row['source']}."
        )
        chunks.append(chunk)
    return chunks

def build_and_save_index():
    """
    Builds a FAISS index from the knowledge base CSV and saves it to disk,
    along with the corresponding text data.
    """
    print("--- Starting Knowledge Base Indexing ---")

    print(f"Loading raw data from: {RAW_DATA_PATH}")
    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ ERROR: Raw data file not found. Please ensure 'knowledge_base.csv' exists in 'data/raw/'.")
        return

    try:
        df = pd.read_csv(RAW_DATA_PATH)
        df.fillna("Not available", inplace=True)
        text_chunks = create_text_chunks(df)
        print(f"✅ Successfully created {len(text_chunks)} text chunks.")
    except Exception as e:
        print(f"❌ ERROR: Failed to load or process CSV file. {e}"); return

    print(f"Loading embedding model: '{EMBEDDING_MODEL_ID}'")
    try:
        model = SentenceTransformer(EMBEDDING_MODEL_ID)
        print("✅ Embedding model loaded.")
        embeddings = model.encode(text_chunks, show_progress_bar=True)
        print(f"✅ Generated {embeddings.shape[0]} embeddings of dimension {embeddings.shape[1]}.")
    except Exception as e:
        print(f"❌ ERROR: Failed to generate embeddings. {e}"); return

    try:
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings, dtype=np.float32))
        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
        print(f"Saving FAISS index to: {INDEX_FILE_PATH}")
        faiss.write_index(index, INDEX_FILE_PATH)
        print("✅ FAISS index saved successfully.")
    except Exception as e:
        print(f"❌ ERROR: Failed to build or save FAISS index. {e}"); return

    try:
        with open(TEXT_DATA_PATH, 'wb') as f:
            pickle.dump(text_chunks, f)
        print(f"✅ Text data saved successfully to: {TEXT_DATA_PATH}")
    except Exception as e:
        print(f"❌ ERROR: Failed to save text data. {e}"); return

    print("\n--- ✅ Knowledge Base Indexing Complete ---")


if __name__ == '__main__':
    build_and_save_index()


