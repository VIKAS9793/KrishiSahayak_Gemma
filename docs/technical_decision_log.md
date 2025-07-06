# Technical Decision Log: KrishiSahayak Web Demo

**Date:** July 6, 2025  
**Status:** Finalized  
**Component:** web_demo

## 1. Objective

The primary objective for this component was to rapidly develop a high-fidelity, interactive web-based prototype. This prototype serves two main purposes:
- To validate the core multimodal AI pipeline (Image + Audio → Diagnosis)
- To provide a functional and impressive demo for stakeholders, showcasing the project's potential before embarking on the more complex native Android development.

## 2. Architectural Decisions

A standard, server-based Python architecture was chosen to prioritize development speed and leverage the mature Python AI ecosystem.

| Component | Technology | Justification |
|-----------|------------|---------------|
| Web Framework | Gradio | Selected for its ability to create rich, interactive ML application interfaces with minimal code, making it ideal for rapid prototyping. |
| Backend Logic | Python 3 | The de-facto standard for ML engineering, providing access to all necessary libraries for inference, audio processing, and search. |
| Serving | FastAPI / Uvicorn | These are the underlying, high-performance web servers used by Gradio to handle user requests efficiently. |

## 3. Model & Inference Strategy

A key decision was made to use different model assets for the web demo and the final Android application, optimizing each for its specific environment.

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

- **Vector Search:** A FAISS index is built from the curated `knowledge_base.csv` using sentence-transformers embeddings.
- **Uncertainty Trigger:** A custom module (`uncertainty.py`) analyzes the model's initial response. If the response is too short or contains keywords indicating uncertainty (e.g., "could be," "not sure"), the RAG pipeline is triggered.

**Benefit:** This adds a layer of robustness. When the base model is not confident, it can retrieve relevant, expert-verified information from our knowledge base to provide a more accurate and trustworthy final answer.

## 5. Conclusion

The chosen architecture and technologies are optimal for the web demo. By keeping the web and mobile tracks separate, we can effectively showcase the project's full potential while ensuring the final Android product is perfectly optimized for its real-world constraints.
