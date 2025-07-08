# Technical Decision Log: KrishiSahayak Web Demo

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

A key decision was made to use a different model asset and inference strategy for the web demo than for the final Android application, optimizing each for its specific environment.

### Web Demo Strategy (Implemented):
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
- **Uncertainty Trigger:** A custom module (`uncertainty.py`) analyzes the model's initial response. If the response is too short or contains keywords indicating uncertainty (e.g., "could be," "not sure"), the RAG pipeline is triggered to provide a source-grounded answer.

**Benefit:** This adds a layer of robustness and demonstrates the explainability features planned for the final product.

## 5. Deployment & Distribution Strategy

The web demo has a distinct deployment model from the final Android app.

- **Web Demo:** Deployed on a standard cloud server or run locally for demonstration purposes. It requires an active internet connection to download the model on first run.
- **Android App:** A fully offline application distributed via P2P methods (SD cards, local file sharing), not the Google Play Store.

## 6. Conclusion

The chosen architecture and technologies are optimal for the web demo. By keeping the web and mobile tracks separate, we can effectively showcase the project's full potential while ensuring the final Android product is perfectly optimized for its real-world constraints. This decision log accurately reflects the technical choices made for this specific prototype component.

---
*Last updated: July 8, 2025*
