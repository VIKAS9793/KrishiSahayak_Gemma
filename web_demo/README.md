# KrishiSahayak+Gemma: Development Tools

> **Development Use Only**: This directory contains development and testing tools for the KrishiSahayak project. These tools are provided for development and testing purposes only and are not part of the production mobile application.

## Purpose
- Test and validate the AI pipeline
- Demonstrate core functionality to stakeholders
- Facilitate development and debugging
- Validate model performance

## 🌟 Features
- Image and audio input for crop diagnosis
- AI-powered diagnosis using Gemma 3B model
- Retrieval-Augmented Generation (RAG) for accurate responses
- Multilingual text-to-speech support

## 🚀 Quick Start

For detailed setup and deployment instructions, including system requirements and troubleshooting, see the [Deployment Guide](DEPLOYMENT_GUIDE.md).

### Basic Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## 📚 Documentation
- [Deployment Guide](DEPLOYMENT_GUIDE.md) - Complete setup and troubleshooting
- [API Reference](docs/API_REFERENCE.md) - API documentation
- [Development Guide](docs/DEVELOPMENT.md) - Contributing and development workflow

## 📁 Project Structure

```
web_demo/
├── app.py                # Main application entry point
├── requirements.txt      # Core production dependencies
├── requirements-dev.txt  # Optional development & monitoring dependencies
└── src/
    ├── api/              # API endpoints and routes
    │   └── routes.py
    ├── pipeline/         # Core AI processing pipeline
    │   ├── __init__.py
    │   ├── inference.py  # Model loading and inference logic
    │   └── uncertainty.py # Uncertainty quantification
    ├── rag/              # Retrieval-Augmented Generation
    │   ├── __init__.py
    │   ├── search.py     # Semantic search implementation
    │   ├── monitoring.py # RAG monitoring utilities
    │   └── performance_monitor.py # Performance tracking
    └── utils/            # Utility functions
        ├── __init__.py
        ├── audio_processing.py  # Audio handling utilities
        └── cache_utils.py      # Caching mechanisms
```

## 🤖 Model Information

This demo uses the `gemma-3n-q4_k_m.gguf` model, which is a 4-bit quantized version of the `google/gemma-3n-E2B-it` model, optimized for efficient inference on consumer hardware.

## 📝 Notes
- These tools require an internet connection to download model weights on first run
- For production deployment, consider using a GPU-accelerated server for better performance
- All sensitive configurations should be managed through environment variables

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
