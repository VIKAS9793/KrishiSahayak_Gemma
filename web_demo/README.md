# KrishiSahayak+Gemma: Web Demo

This directory contains the source code for the web-based demonstration of the KrishiSahayak project. It uses a Gradio interface to provide a user-friendly way to interact with the multimodal AI pipeline.

## Features
- Image and audio input for crop diagnosis.
- AI-powered diagnosis using the `google/gemma-3n-E2B-it` model.
- Retrieval-Augmented Generation (RAG) to improve accuracy when the model is uncertain.
- Text-to-speech output in Hindi.

## Setup and Execution

1. **Create a Virtual Environment (Windows):**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python app.py
   ```
   The application will start, and you can access it through the provided local or public URL.

## Project Structure

```
web_demo/
├── app.py                # Main application entry point
├── requirements.txt      # Python dependencies
├── pipeline/             # Core AI processing pipeline
│   ├── __init__.py
│   ├── inference.py     # Model loading and inference logic
│   └── uncertainty.py   # Uncertainty quantification
├── rag/                  # Retrieval-Augmented Generation
│   ├── __init__.py
│   └── search.py        # Semantic search implementation
└── utils/               # Utility functions
    ├── __init__.py
    └── audio_processing.py  # Audio handling utilities
```

## Model Information
For details about the model used in this demo, see [MODEL_CARD.md](MODEL_CARD.md).

## License
This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
