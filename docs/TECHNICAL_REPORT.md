# KrishiSahayak+Gemma: Technical Report & Data Specification

**Version:** 1.2  
**Date:** July 8, 2025  
**Status:** End of Phase 1: Asset Production & Optimization

## 1. Project Mission & Overview

KrishiSahayak+Gemma is an engineering initiative to provide farmers in India with a **100% offline, reliable, and user-friendly Android application** that operates efficiently on low-resource smartphones (≤ 2GB RAM).

This document provides a technical overview at the conclusion of Phase 1, which focused on the successful creation and validation of the production-ready AI assets that will power the final application.

## 2. System Architecture: Dual-Track Approach

The project follows a strategic two-track development approach to balance rapid prototyping with production readiness.

* **Web Demo Prototype:** A server-based Gradio application using the Hugging Face `transformers` library to showcase the AI's maximum potential in an unconstrained environment.
* **Android Production App:** The primary goal of the project. A native Android app using a pre-quantized `.gguf` model and the `llama.cpp` C++ engine for maximum offline performance.

## 3. Core AI Asset: `gemma-3n-q4_k_m.gguf`

The central component of the Android application is a highly optimized version of Google's Gemma model.

* **Base Model:** `google/gemma-3n-E2B-it` (4.46 Billion Parameters)
* **Quantization:** 4-bit (`Q4_K_M`)
* **Final Size:** **2.59 GiB** (68.8% reduction from FP16)
* **Performance:** **48.8% faster** inference time compared to the FP16 baseline.

This asset was produced via a robust pipeline on a high-performance GCP instance, and its performance has been rigorously validated (see `docs/model_card.md` for full metrics).

## 4. Data Architecture & Phased Strategy

The project utilizes a sophisticated data pipeline and a phased strategy to ensure both rapid development and high-quality, relevant data in the final product.

* **MVP Development (Current Phase):** To de-risk the engineering effort, the initial Android MVP will be built using the **generic `knowledge_base_v0_generic_46-class` dataset**. This allows for immediate development and testing of the core offline technology stack.
* **Production Data (Future Phase):** The long-term vision is to use **expert-curated Regional Data Packs**. This will be a separate phase involving manual curation with agricultural scientists to ensure maximum accuracy. The initial focus for this effort will be the **6 pilot states** outlined in `docs/REGIONAL_COVERAGE.md`.

## 5. Reliability: RAG Fallback System

The application implements a Retrieval-Augmented Generation (RAG) system to enhance reliability.

* **Uncertainty Detection:** A module (`uncertainty.py`) analyzes the model's initial response for signs of low confidence.
* **Contextual Retrieval:** If uncertainty is detected, the system performs a semantic search on the local `.faiss` index to retrieve relevant, verified text chunks.
* **Reprompting:** The original query is combined with the retrieved context and sent back to the model for a final, source-grounded diagnosis.

## 6. Project Status & Next Steps

* **Current Status:** **Phase 1 (Asset Production & Optimization) is complete.**
* **Next Step:** **Phase 2 (Android App Development).** The focus now shifts to building the native Android application and integrating the validated AI assets using the generic dataset for initial functionality.

---
*Last updated: July 8, 2025*