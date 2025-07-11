# Technical Decision Log: KrishiSahayak Core Architecture

**Version:** 2.0  
**Date:** July 8, 2025  
**Status:** Finalized  
**Component:** web_demo

## 1. Objective

The primary objective for this component was to rapidly develop a high-fidelity, interactive web-based prototype. This prototype serves two main purposes:

1. To validate the core multimodal AI pipeline (Image + Audio → Diagnosis).
2. To provide a functional and impressive demo for stakeholders, showcasing the project's potential before embarking on the more complex native Android development.

## 2. Architectural Decisions

A standard, server-based Python architecture was chosen to prioritize development speed and leverage the mature Python AI ecosystem.

| Component | Technology | Justification |
|-----------|------------|---------------|
| Web Framework | Gradio | Selected for its ability to create rich, interactive ML application interfaces with minimal code, making it ideal for rapid prototyping. |
| Backend Logic | Python 3 | The de-facto standard for ML engineering, providing access to all necessary libraries for inference, audio processing, and search. |
| Serving | FastAPI / Uvicorn | These are the underlying, high-performance web servers used by Gradio to handle user requests efficiently. |

## 3. Model & Inference Strategy

A key decision was made to optimize the model assets and inference strategy for the production Android application, focusing on performance and resource efficiency.

### Core AI Strategy (Implemented):
- **Model Source:** The base `google/gemma-3n-E2B-it` model is downloaded directly from the Hugging Face Hub at runtime.
- **Inference Library:** The Hugging Face `transformers` library is used to run inference.
- **Quantization:** BitsAndBytes is used to perform on-the-fly 4-bit quantization.

**Justification:** This strategy is ideal for a prototype. It leverages powerful server-side hardware to showcase the model's maximum quality and capabilities with minimal setup complexity.

### Android App Strategy (Separate Track):
- **Model Source:** The pre-quantized `gemma-3n-q4_k_m.gguf` asset.
- **Inference Library:** The native `llama.cpp` C++ engine.

**Justification:** This strategy is essential for the final product. It prioritizes offline performance, small size, and low RAM usage, which are the core requirements for the target mobile devices.

## 4. Data & Reliability Strategy

To enhance the reliability and explainability of the demo, a Retrieval-Augmented Generation (RAG) pipeline was implemented as a fallback mechanism.

- **Vector Search:** A FAISS index is built from the curated `knowledge_base_v0_generic_46-class.csv` using sentence-transformers embeddings.

**Benefit:** This adds a layer of robustness and demonstrates the explainability features planned for the final product.

## 5. Deployment & Distribution Strategy

The architecture is designed with a focus on the Android application's requirements:

- **Offline-First Design:** All necessary assets are bundled in the APK
- **Optimized for Mobile:** The model is pre-quantized and optimized for mobile devices with limited resources
- **Performance Focus:** Emphasis on fast inference times and low memory usage

The chosen architecture and technologies ensure the final Android product is perfectly optimized for its real-world constraints, providing a responsive and reliable experience for end-users in low-connectivity environments.

---
*Last updated: July 8, 2025*
