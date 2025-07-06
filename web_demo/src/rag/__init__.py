"""
Retrieval-Augmented Generation (RAG) components for KrishiSahayak.

This package provides functionality for semantic search and knowledge base integration
to enhance the AI's responses with relevant information.
"""
from .search import search_knowledge_base, load_search_dependencies

# Note: build_faiss_index has been moved to asset_preparation/build_index.py
__all__ = ['search_knowledge_base', 'load_search_dependencies']
