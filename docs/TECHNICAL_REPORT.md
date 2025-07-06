# KrishiSahayak Project: Technical Report & Data Specification

**Version:** 1.0  
**Date:** July 6, 2025  
**Status:** End of Phase 1: Asset Production & Optimization

## 1. Project Overview

This document provides a verified technical overview of the KrishiSahayak+Gemma project at the conclusion of Phase 1. The primary achievement of this phase was the successful creation and validation of a production-ready, quantized AI model and its associated data assets, which will be used to power the final Android application.

## 2. Core AI Asset: gemma-3n-q4_k_m.gguf

The central component of the system is a highly optimized version of Google's Gemma model, prepared for offline mobile deployment.

- **Base Model:** `google/gemma-3n-E2B-it` (4.46 Billion Parameters)
- **Inference Engine:** `llama.cpp`
- **Final Format:** GGUF with Q4_K_M 4-bit quantization.
- **Final Size:** 2.59 GiB

This asset was produced via a robust pipeline on a high-performance GCP instance, and its performance has been validated (see [Model Card](web_demo/MODEL_CARD.md) for full metrics).

## 3. Data Architecture

The project utilizes a structured knowledge base to enable the Retrieval-Augmented Generation (RAG) system, which acts as a fallback to improve model reliability.

### 3.1. Primary Data Source: knowledge_base.csv

This file contains the expert-verified information used for the RAG system.

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| disease_name | String | A unique identifier in the format `Plant___Disease`. | `Tomato___Early_Blight` |
| symptoms | Text | A detailed description of the disease's visual symptoms. | `"Leaves have 'bull's-eye' lesions..."` |
| remedy | Text | Actionable management and treatment advice. | `"Practice crop rotation... Apply fungicides..."` |
| source | String | The source from which the information was verified. | `"Vikaspedia ; UC IPM"` |

### 3.2. RAG Index Specification

The knowledge base is converted into a vector index for fast semantic search.

- **Vectorization Model:** `all-MiniLM-L6-v2`
- **Vector Dimensions:** 384
- **Index File:** `knowledge_base.faiss` (FAISS CPU Index)
- **Text Data File:** `knowledge_base_text.pkl`

## 4. Web Demo Component

A separate web-based prototype exists for demonstration purposes. It is important to note that it uses a different technology stack than the final Android product to prioritize rapid development.

- **Framework:** Gradio
- **Inference:** `transformers` library with on-the-fly BitsAndBytes quantization.
- **Purpose:** To showcase the multimodal pipeline and core logic in a server-based environment. It does not use the .gguf asset.

## 5. Project History & Status (Changelog)

### [v0.1.0] - 2025-07-06
- **Completed:** All Phase 1 objectives.
- **Added:** Production-ready .gguf model asset.
- **Added:** Validated FAISS index and SQLite database assets.
- **Added:** Comprehensive Model Card with performance benchmarks.
- **Added:** Refactored project structure with clear separation between `web_demo` and `asset_preparation`.
- **Status:** Ready to begin Phase 2: Android App Development.

### [v0.0.1] - 2025-06-30
- **Added:** Initial project repository and documentation.
- **Added:** Curated `knowledge_base.csv`.

---
*Document last updated: July 6, 2025*
