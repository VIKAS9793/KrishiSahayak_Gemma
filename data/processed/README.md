# Processed Data Files

This directory contains pre-processed knowledge base files used by the KrishiSahayak+Gemma system. These files are generated from the curated knowledge base and are optimized for fast searching and retrieval.

## Getting the Files

### Option 1: Download from GitHub Releases (Recommended)

1. Go to the [GitHub Releases](https://github.com/VIKAS9793/KrishiSahayak_Gemma/releases) page
2. Download the `KrishiSahayak_KB_v0.10.0.zip` file
3. Extract the contents to this directory

### Option 2: Generate from Source

If you need to regenerate these files:

```bash
# Make sure you have the source CSV file in data/raw/
python scripts/process_knowledge_base.py --input data/raw/knowledge_base_v0_generic_46-class.csv --output data/processed/
```

## File Descriptions

After extracting `KrishiSahayak_KB_v0.10.0.zip`, you should have these files:

- `knowledge_base_v0_generic_46-class.csv`: The curated knowledge base in CSV format
- `knowledge_base_v0_generic_46-class.faiss`: FAISS index for semantic search
- `knowledge_base_v0_generic_46-class.sqlite`: SQLite database for efficient querying
- `knowledge_base_v0_generic_46-class_text.pkl`: Serialized text data for the RAG system

## Note

These files are not version-controlled due to their size. Always download the latest version from GitHub Releases for production use.
