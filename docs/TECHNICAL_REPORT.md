# KrishiSahayak+Gemma: Technical Report

**Version:** 1.3  
**Date:** July 12, 2025  
**Status:** End of Phase 1: Asset Production & Optimization

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [AI Pipeline](#ai-pipeline)
4. [Model Optimization](#model-optimization)
5. [Data Strategy](#data-strategy)
6. [RAG Implementation](#rag-implementation)
7. [Performance Metrics](#performance-metrics)
8. [Development Tools](#development-tools)
9. [Next Steps](#next-steps)

## 1. Project Overview

The KrishiSahayak+Gemma project is an engineering initiative to deliver a **100% offline, reliable, and user-friendly Android application** that operates efficiently on low-resource smartphones (≤ 2GB RAM) for farmers in India.

For more details on the project vision and strategy, see [STRATEGY_AND_ROADMAP.md](STRATEGY_AND_ROADMAP.md).

## 2. System Architecture

The project follows a dual-track development approach to balance rapid prototyping with production readiness:

### 2.1 Development Tools

A web-based development interface for testing and validating the AI pipeline. See [web_demo/README.md](../web_demo/README.md) for details.

### 2.2 Production System

The primary goal of the project. A native Android app using a pre-quantized `.gguf` model and the `llama.cpp` C++ engine for maximum offline performance.

The project follows a dual-track development approach:

1. **Development Tools:** A web-based interface for testing and validating the AI pipeline. See [web_demo/README.md](../web_demo/README.md) for details.
2. **Production System:** A native Android app using a pre-quantized `.gguf` model and the `llama.cpp` C++ engine for maximum offline performance.

## 3. Core AI Asset for Android: `gemma-3n-q4_k_m.gguf`

The central component of the Android application is a highly optimized version of Google's Gemma model.

* **Model File:** `gemma-3n-q4_k_m.gguf`
* **Base Model:** `google/gemma-3n-E2B-it` (4.46 Billion Parameters)
* **Quantization:** 4-bit (`Q4_K_M`)
* **Final Size:** **2.60 GiB** (a 68.7% reduction from the 8.31 GiB FP16 version)
* **Performance:** While the total task time is slightly longer due to the initial dequantization overhead on the CPU, the massive reduction in file size is the critical optimization for mobile deployment.

![Model Loading Performance](images/model_loading.png)
*Figure 2: Model loading performance metrics across different devices*

## 4. Data Strategy

The project has adopted a phased data strategy to de-risk development and ensure the final data quality is exceptionally high.

### 4.1 MVP Development

To accelerate development, the initial Android MVP will be built using the generic **46-class dataset** (`knowledge_base_v0_generic_46-class`). This allows us to build and test the core offline technology stack without being blocked by the long data curation timeline.

### 4.2 Production Approach

The final, production-ready solution will use **expert-curated Regional Data Packs**. This will be a separate, future phase involving manual curation with agricultural scientists to ensure the highest level of accuracy. **No AI-generated data will be used in the final production knowledge base.**

For detailed regional coverage strategy, see [REGIONAL_COVERAGE.md](REGIONAL_COVERAGE.md).

For detailed data strategy and regional coverage, see:
- [REGIONAL_COVERAGE.md](REGIONAL_COVERAGE.md)
- [VERSIONING.md](VERSIONING.md)

## 5. Reliability: RAG Fallback System

The application implements a Retrieval-Augmented Generation (RAG) system to enhance reliability.

![RAG Fallback Pipeline](images/RAG%20fallback%20pipeline%20in%20action.png)
*Figure 5.1: RAG fallback pipeline in action*

### RAG System Components

1. **Uncertainty Detection**
   - A module (`uncertainty.py`) analyzes the model's initial response for signs of low confidence.
   - Example of uncertainty detection:
   ![Uncertain Query](images/Uncertain%20query.png)
   *Figure 5.2: Example of an uncertain query*

2. **Contextual Retrieval**
   - If uncertainty is detected, the system performs a semantic search on the local `.faiss` index to retrieve relevant, verified text chunks.
   - Example output:
   ![RAG Output 1](images/RAG%20based%20output_1.png)
   *Figure 5.3: RAG output example 1*

3. **Reprompting**
   - The original query is combined with the retrieved context and sent back to the model for a final, source-grounded diagnosis.
   - Example output:
   ![RAG Output 2](images/RAG%20based%20output_2.png)
   *Figure 5.4: RAG output example 2*

This system ensures that the AI provides reliable, source-grounded responses by leveraging local knowledge base data when uncertain about its initial response.

## 7. Next Steps

* **Current Status:** **Phase 1 (Asset Production & Optimization) is complete.**
* **Next Step:** **Phase 2 (Android App Development).** The focus now shifts to building the native Android application and integrating the validated AI assets using the generic dataset for initial functionality.

---
*Last updated: July 12, 2025*

* **Current Status:** **Phase 1 (Asset Production & Optimization) is complete.**
* **Next Step:** **Phase 2 (Android App Development).** The focus now shifts to building the native Android application and integrating the validated AI assets using the generic dataset for initial functionality.