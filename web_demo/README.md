# KrishiSahayak+Gemma: Development Tools

> **Development Use Only**: This directory contains development and testing tools for the KrishiSahayak project. These tools are provided for development and testing purposes only and are not part of the production mobile application.

For the project's mission and technical details, please refer to the main documentation in the [docs](../docs/) directory.

## Purpose
- Test and validate the AI pipeline
- Demonstrate core functionality to stakeholders
- Facilitate development and debugging
- Validate model performance

For detailed technical architecture and implementation, see the [Technical Report](../docs/TECHNICAL_REPORT.md).

## 🌟 Features
- Image and audio input for crop diagnosis
- AI-powered diagnosis using Gemma 3B model
- Retrieval-Augmented Generation (RAG) for accurate responses
- Multilingual text-to-speech support

## 📸 Web Demo Interface

The web demo provides a user-friendly interface for testing and demonstrating the core functionality of KrishiSahayak+Gemma. Here's a quick tour of the interface:

![Web Demo Home](../docs/images/web%20demo_1.png)
*Figure 1: Main interface with image upload and audio input options*

![Web Demo Diagnosis](images/web%20demo_2.png)
*Figure 2: Real-time diagnosis with RAG support*

![Web Demo Results](images/web%20demo_3.png)
*Figure 3: Detailed diagnosis results with confidence scores*

![Web Demo Audio](images/web%20demo_4.png)
*Figure 4: Audio input and transcription interface*

![Web Demo Multilingual](images/web%20demo_5.png)
*Figure 5: Multilingual support and text-to-speech options*

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

For detailed model specifications, see the [Model Card](../docs/model_card.md).

## 📝 Notes
- These tools require an internet connection to download model weights on first run
- For production deployment, consider using a GPU-accelerated server for better performance
- All sensitive configurations should be managed through environment variables

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.
