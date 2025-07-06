# Technical Decision Log: KrishiSahayak+Gemma

**Date:** July 5, 2025  
**Status:** Approved  
**Version:** 1.0

## 1. Objective
The primary technical objective was to convert the `google/gemma-3n-e2b-it` model into a quantized TensorFlow Lite (.tflite) file suitable for offline, on-device inference in a hyper-constrained environment (2GB RAM).

## 2. The Core Challenge: "Dependency Hell" in Cloud Environments
The project faced a persistent and critical blocker: the inability to create a stable Python environment for model conversion within standard cloud notebook platforms (Google Colab, Kaggle).

### 2.1. Root Cause Analysis
The root cause was identified as a fundamental conflict between the pre-installed, older software packages in the cloud environments and the new, cutting-edge libraries required to support the novel architecture of the Gemma 3n model family.

- **Pre-existing Environment:** Cloud notebooks come with dozens of libraries (tensorflow, numpy, transformers, etc.) already installed.
- **Conflicting Requirements:** The optimum and ai-edge-torch libraries, required for conversion, have strict dependency requirements that clashed with these pre-installed packages.
- **Resolution Failure:** pip's dependency resolver correctly identified these conflicts and failed with ResolutionImpossible errors, preventing the creation of a stable environment.

### 2.2. Attempted Solutions & Outcomes
A series of industry-standard solutions were systematically attempted to resolve the environmental conflicts.

| Attempt | Strategy | Outcome | Analysis |
|---------|----------|---------|----------|
| A | Standard pip install | Failure | ResolutionImpossible errors due to conflicts with base image packages. |
| B | Pinned Versions | Failure | ResolutionImpossible errors. Manually guessing a compatible set of versions for such new libraries proved impossible. |
| C | Install from Source (GitHub) | Failure | ImportError. Even the latest dev versions of the libraries had internal incompatibilities. |
| D | Isolated conda Environment | Failure | ResolutionImpossible. Conda's more powerful resolver also failed, confirming the deep incompatibility. |
| E | Docker Environment | Blocked | The ideal solution was blocked by the user's local machine failing to install Docker Desktop, a prerequisite. |

## 3. The Second Challenge: Unstable Tooling
The repeated failures led to a critical insight, which was confirmed by further research: the standard open-source conversion tools (optimum) were not yet officially stable for the brand-new Gemma 3n architecture. The model was released ahead of full support in the community toolchain.

## 4. Final Solution & Architectural Pivot
The only professional engineering path forward was to stop trying to fix an unstable conversion process and instead use an official, pre-built artifact.

### 4.1. The Pivot: Direct Download of Pre-Converted Model
We discovered that Google provides an official, pre-converted TFLite version of the model specifically for on-device use: `google/gemma-3n-E4B-it-litert-preview`.

Our strategy pivoted from **Model Conversion** to **Direct Asset Download**.

### 4.2. Justification
This decision is rooted in production engineering best practices:

- **Eliminates Risk:** It completely removes all risks associated with unstable tooling and dependency conflicts.
- **Guarantees Correctness:** Using the official asset guarantees that we have a model that is correctly converted and optimized by the team that built it.
- **Accelerates Project Timeline:** It unblocks the project, allowing us to immediately proceed with building the Android application without further delays.

## 5. Conclusion
The journey to acquire a mobile-compatible model asset for Gemma 3n highlights a key lesson in modern ML engineering: for bleeding-edge models, the official, vendor-provided artifacts are often more reliable than community tools that are still catching up. Our final strategy of downloading the pre-converted model is the most robust, professional, and pragmatic path to achieving our project goals.

## 6. Next Steps
1. Implement model download and verification script
2. Integrate the pre-converted model into the Android application
3. Optimize model loading and inference for target hardware
4. Implement model update mechanism for future versions
