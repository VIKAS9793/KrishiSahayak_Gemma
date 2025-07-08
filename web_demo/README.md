# KrishiSahayak+Gemma: Web Demo

This directory contains the source code for the web-based demonstration of the KrishiSahayak project. It uses a Gradio interface to provide a user-friendly way to interact with the multimodal AI pipeline.

## 🌟 Features
- Image and audio input for crop diagnosis
- AI-powered diagnosis using the `google/gemma-3n-E2B-it` model with on-the-fly 4-bit quantization
- Retrieval-Augmented Generation (RAG) to improve accuracy when the model is uncertain
- Text-to-speech output in Hindi

## 🚀 Setup and Execution

### 1. Prerequisites
- Python 3.8+
- `git`

### 2. Create a Virtual Environment
It is a critical best practice to use a Python virtual environment to avoid conflicts with system-wide packages.

```bash
# Create the virtual environment
python -m venv venv

# Activate the environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### 3. Install Dependencies
This project separates production dependencies from optional development/monitoring packages.

```bash
# Install the core packages required to run the demo
pip install -r requirements.txt

# (Optional) To install tools for monitoring and advanced deployment:
pip install -r requirements-dev.txt
```

### 4. Run the Application
```bash
# Launch the Gradio web server
python app.py
```

The application will start, and you can access it through the local URL provided in your terminal (e.g., http://127.0.0.1:7860).

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

This demo uses the `google/gemma-3n-E2B-it` model with on-the-fly quantization via the BitsAndBytes library. This is distinct from the pre-quantized `.gguf` asset used by the final Android application.

## 📝 Notes
- The web demo requires an internet connection to download the model weights on first run
- For production deployment, consider using a GPU-accelerated server for better performance
- All sensitive configurations should be managed through environment variables

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
