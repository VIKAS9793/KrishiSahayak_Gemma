# Technical Decision Log: KrishiSahayak Web Demo

**Version:** 1.1  
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

- **Vector Search:** A FAISS index is built from the curated `knowledge_base_v0_generic_46-class.csv` using sentence-transformers embeddings.
- **Data Versioning:** The initial dataset (v0) has been archived in `data/_archive/` with the following files:
  - `knowledge_base_v0_generic_46-class.csv` - Original structured data
  - `knowledge_base_v0_generic_46-class.faiss` - Pre-built FAISS index
  - `knowledge_base_v0_generic_46-class_text.pkl` - Processed text data
  - `knowledge_base_v0_generic_46-class.sqlite` - SQLite database for mobile
- **Uncertainty Trigger:** A custom module (`uncertainty.py`) analyzes the model's initial response. If the response is too short or contains keywords indicating uncertainty (e.g., "could be," "not sure"), the RAG pipeline is triggered.

**Benefit:** This adds a layer of robustness. When the base model is not confident, it can retrieve relevant, expert-verified information from our knowledge base to provide a more accurate and trustworthy final answer. The versioned archive ensures reproducibility and makes it easy to maintain different dataset versions.

### 2025-07-07: Knowledge Base Versioning and Archiving Strategy

#### 1. Versioned Data Storage
- **Decision**: Implement a structured versioning system for all data assets
- **Reason**: To enable tracking changes, support rollbacks, and maintain reproducibility
- **Details**:
  - All data files now follow the pattern: `knowledge_base_v{MAJOR}_{MINOR}_[TYPE]_[DETAILS].{EXT}`
  - Current version: `v0_generic_46-class`
  - Files stored in `data/_archive/` directory

#### 2. Updated File Structure
- **Changes**:
  - Moved all knowledge base files to versioned names in `data/_archive/`
  - Updated all code references to use versioned paths
  - Created comprehensive documentation in `docs/VERSIONING.md`

#### 3. Impact and Migration
- **Affected Components**:
  - Web demo configuration
  - Asset preparation scripts
  - Documentation
- **Migration Path**:
  - All systems now reference the versioned files
  - Old file paths have been removed
  - Documentation updated to reflect current structure

#### 4. Future Considerations
- Automated version bumping for data updates
- Integration with CI/CD pipeline
- Validation tests for data consistency

## 5. Deployment & Distribution Strategy

The two project tracks have distinct deployment models.

### Web Demo:
- Deployed on a standard cloud server or run locally for demonstration purposes.
- Requires an active internet connection to download the model on first run.

### Android App:
- A fully offline application.
- Not distributed through the Google Play Store.
- Distribution method:
  - Final .apk file will be distributed through a network of trusted partners (NGOs, local agricultural centers).
  - Updates (containing new models or databases) will be delivered to partners.
  - Partners will distribute updates to farmers via P2P methods like SD cards or local file sharing.
- **Benefits:**
  - Ensures application accessibility in areas with no internet connectivity.
  - Maintains the ability to push updates through trusted local networks.
  - Reduces data costs and infrastructure requirements for end-users.

## 6. Conclusion

The chosen architecture and technologies are optimal for the web demo. By keeping the web and mobile tracks separate, we can effectively showcase the project's full potential while ensuring the final Android product is perfectly optimized for its real-world constraints.
