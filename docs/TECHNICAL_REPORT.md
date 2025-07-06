# KrishiSahayak+Gemma: Technical Report & Data Specification

**Version:** 1.1  
**Date:** July 6, 2025  
**Status:** End of Phase 1: Asset Production & Optimization

## 1. Project Mission & Overview

KrishiSahayak+Gemma is an engineering initiative designed to address a critical challenge: providing farmers in low-connectivity regions of India with access to advanced AI-driven agricultural advice. The primary objective is to deliver a 100% offline, reliable, and user-friendly Android application that operates efficiently on low-resource smartphones (≤ 2GB RAM).

This document provides a comprehensive technical overview of the project at the conclusion of Phase 1, which focused on the successful creation and validation of production-ready AI assets, including a quantized model and knowledge base that will power the final Android application.

## 2. System Architecture: Dual-Track Approach

The project follows a strategic two-track development approach to balance rapid prototyping with production readiness.

### 2.1 Web Demo Prototype
- **Technology Stack:** Python, Gradio, Hugging Face Transformers
- **Purpose:** Showcase full AI capabilities in a server environment
- **Key Features:**
  - On-the-fly quantization
  - Internet connectivity for model downloads
  - Rapid iteration and demonstration

### 2.2 Android Production App
- **Technology Stack:** Native Android, C++ (llama.cpp), pre-quantized .gguf model
- **Focus:** Extreme optimization for offline performance
- **Key Features:**
  - Pre-quantized model integration
  - Native C++ inference engine
  - Custom Android OS integration
  - Minimal resource consumption

## 3. Core AI Asset: gemma-3n-q4_k_m.gguf

The central component of the system is a highly optimized version of Google's Gemma model, prepared for offline mobile deployment.

### 3.1 Gemma-3B Model
- **Model Name:** gemma-3n-q4_k_m.gguf
- **Base Model:** google/gemma-3n-E2B-it
- **Quantization:** 4-bit (Q4_K_M)
- **Final Size:** 2.59GB (68.8% reduction from FP16)
- **Performance:** 48.8% faster inference time compared to FP16
- **Memory Usage:** Optimized for ≤2GB RAM devices

This asset was produced via a robust pipeline on a high-performance GCP instance (8-core, 32GB RAM), and its performance has been rigorously validated (see [Model Card](model_card.md) for full metrics).

## 4. Data Architecture & Knowledge Engineering

The project utilizes a sophisticated data pipeline to ensure accurate and reliable agricultural advice.

### 4.1. Knowledge Base Development

**Challenge:** Ensuring accurate and contextually relevant agricultural advice for Indian farmers.

**Solution:**
- Implemented a generative pipeline (`generate_knowledge_base_gemma.py`) using Gemma
- Established human-in-the-loop curation process (documented in `Indian Agriculture Disease Data Curation.docx`)
- Developed comprehensive validation scripts for data quality assurance

### 4.2. Primary Data Source: knowledge_base.csv

This file contains the expert-verified information used for the RAG system.

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| disease_name | String | A unique identifier in the format `Plant___Disease`. | `Tomato___Early_Blight` |
| symptoms | Text | A detailed description of the disease's visual symptoms. | `"Leaves have 'bull's-eye' lesions..."` |
| remedy | Text | Actionable management and treatment advice. | `"Practice crop rotation... Apply fungicides..."` |
| source | String | The source from which the information was verified. | `"Vikaspedia ; UC IPM"` |

### 4.3. RAG System Implementation

The knowledge base powers a Retrieval-Augmented Generation (RAG) system that enhances model reliability.

- **Vectorization Model:** `all-MiniLM-L6-v2`
- **Vector Dimensions:** 384
- **Index File:** `knowledge_base.faiss` (FAISS CPU Index)
- **Text Data File:** `knowledge_base_text.pkl`
- **Uncertainty Detection:** Heuristic-based confidence scoring
- **Fallback Mechanism:** Contextual reprompting with retrieved information

## 5. Advanced AI Pipeline

### 5.1 RAG Fallback System

**Challenge:** Preventing confidently incorrect answers when the model is uncertain.

**Solution:**
- Implemented a sophisticated RAG system with uncertainty detection
- Components:
  - `uncertainty.py`: Detects low-confidence answers using heuristics
  - `build_index.py` and `search.py`: Create and query FAISS vector index
  - Fallback mechanism for retrieving relevant context

### 5.2 Model Optimization Pipeline

**Challenge:** Deploying an 11GB cloud-based AI model on 2GB RAM devices with no internet.

**Solutions:**
1. **Environment Setup:**
   - High-performance GCP VM (8-core, 32GB RAM)
   - Stable build environment

2. **Model Quantization:**
   - Utilized llama.cpp C++ library
   - 4-bit (Q4_K_M) quantization
   - 69% size reduction, 49% speed improvement

### 5.3 Web Demo Component

A separate web-based prototype exists for demonstration purposes.

- **Framework:** Gradio
- **Inference:** `transformers` library with on-the-fly quantization
- **Purpose:** Showcase core functionality in a server environment
- **Note:** Uses different technology stack than the final Android product

## 6. Project Roadmap & Status

### Phase 1: Asset Production & Optimization (Completed)
- **v0.1.0 - 2025-07-06**
  - Production-ready .gguf model asset
  - Validated FAISS index and SQLite database
  - Comprehensive Model Card with benchmarks
  - Refactored project structure
  - **Status:** Phase 1 objectives completed

- **v0.0.1 - 2025-06-30**
  - Initial repository setup
  - Curated `knowledge_base.csv`

### Phase 2: Android App Development (Upcoming)
- Native Android application development
- Integration of quantized model
- Offline-first implementation
- Field testing and validation

### Phase 3: Field Testing & Ecosystem Deployment

#### Targeted Initial Deployment
- **Controlled Rollout**:
  - Initial APK distribution to select test users (agricultural agents, partner farmers)
  - Focused on gathering quality feedback
  - Limited to trusted network for controlled testing

#### Offline Distribution Network
- **P2P Distribution**:
  - APK and model updates via SD cards
  - Network of NGO partners and local contacts
  - No internet dependency for distribution

#### Feedback Collection
- **Initial Validation**:
  - Performance metrics collection
  - Accuracy assessment in real-world conditions
  - Usability feedback from actual users

### Phase 4: Continuous Improvement & Scaling

#### Feedback Pipeline
- **Structured Data Collection**:
  - System for gathering user queries and feedback
  - Performance monitoring and error tracking
  - Localized agricultural challenge identification

#### Model Evolution
- **Continuous Learning**:
  - Regular model retraining with field data
  - Fine-tuning for regional specificities
  - Accuracy improvements based on real-world usage

#### Update Distribution
- **Sustained Offline Updates**:
  - Regular update packages for Krishi-Mitra network
  - Versioned releases with changelogs
  - Backward compatibility maintenance

#### Long-term Vision
- **Self-Sustaining Cycle**:
  1. Deploy → 2. Gather Feedback → 3. Improve AI → 4. Re-deploy
- **Community-Driven Enhancement**:
  - Local agricultural expertise integration
  - Regional adaptation and expansion
  - Continuous value addition for end-users

## 7. Conclusion

The KrishiSahayak+Gemma project demonstrates how careful engineering and optimization can make advanced AI accessible in resource-constrained environments. By successfully addressing the challenges of model optimization, offline functionality, and resource constraints, we have created a robust solution that brings AI capabilities to underserved farming communities.

The completion of Phase 1 has laid a strong foundation for the Android application development in Phase 2. The project's dual-track approach has allowed for rapid prototyping while ensuring the final product meets the strict requirements of offline operation on low-resource devices.
