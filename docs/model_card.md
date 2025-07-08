# Model Card: KrishiSahayak Android Asset v1.0

**Model Name:** gemma-3n-q4_k_m.gguf  
**Version:** 1.0  
**Date:** July 8, 2025  
**Author:** KrishiSahayak AI Engineering Team

## 1. Model Details

This model is a 4-bit quantized version of Google's Gemma 3n, optimized for high-performance, offline inference on resource-constrained devices.

- **Base Model:** google/gemma-3n-E2B-it
- **Model Architecture:** gemma3n (4.46 Billion Parameters)
- **Model Format:** GGUF (for use with llama.cpp)
- **Quantization Method:** Q4_K_M (4-bit, K-Means)

## 2. Intended Use

**Primary Use-Case:** To serve as the core reasoning engine for the KrishiSahayak Android application. It provides offline diagnostic advice for common agricultural issues based on text descriptions from users.

**Target Users:** Rural farmers in India using low-resource Android smartphones (≤ 2GB RAM).

**Out-of-Scope Uses:** This model is an informational aid and is not a substitute for professional agronomic advice or scientific testing. It must not be used for high-stakes financial, medical, or safety-critical decisions.

## 3. Performance & Evaluation

The model was rigorously benchmarked against its un-quantized FP16 version to validate performance trade-offs.

### Evaluation Setup
- **Hardware:** Google Cloud Platform (GCP) n2-standard-8 instance (8 vCPUs, 32 GB RAM).
- **Test Data:** A curated set of 15 questions representing common agricultural queries in the Indian context.
- **Inference Engine:** llama.cpp (Build: 5834)

### Quantitative Metrics

The Q4_K_M model provides significant improvements in size and speed, which are mandatory for mobile deployment.

| Metric | FP16 Model (Baseline) | Q4_K_M Model (Production) | Improvement |
|--------|----------------------|--------------------------|-------------|
| File Size | 8.30 GiB | 2.59 GiB | -68.8% |
| Total Task Time | ~239.4 seconds | ~122.6 seconds | -48.8% |

### Qualitative Analysis

The quantized model's diagnostic accuracy and the quality of its advice were maintained. Side-by-side comparisons showed that the Q4_K_M model provides the same core diagnostic information as the FP16 baseline, with only a minor reduction in verbosity. No critical information was lost.

## 4. Limitations & Ethical Considerations

- **Risk of Inaccuracy:** The model can produce factually incorrect or incomplete information ("hallucinations"). A misdiagnosis could lead to incorrect crop treatment.

- **Required Mitigation:** The user-facing application must display a prominent disclaimer before every use, stating that the model is an advisory tool and a local expert should be consulted for definitive advice.

- **Data Bias:** The model's knowledge is based on its general training data and our generic 46-class knowledge base for the MVP. It may lack knowledge of hyper-local or newly emerging pests and diseases. This will be addressed in future phases with expert-curated regional data packs.

## 5. How to Use

**Deployment:** This model asset (gemma-3n-q4_k_m.gguf) is intended to be bundled with the KrishiSahayak Android application and run via a native llama.cpp inference engine integrated through the Android NDK.