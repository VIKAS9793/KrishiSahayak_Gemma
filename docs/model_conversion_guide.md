# Gemma Model Conversion and Quantization Guide

**Version:** 0.11.0  
**Date:** July 10, 2025

## Purpose
This guide documents the definitive process for converting and quantizing the Google Gemma 3n model into a deployment-ready asset for the KrishiSahayak application.

## 1. Background: The Strategic Pivot to a Dedicated Build Environment

A key technical challenge in this project was establishing a stable and reproducible environment for the model asset pipeline.

**Initial Approach & Limitations:**  
Initial attempts to perform the conversion in standard cloud notebook environments (e.g., Google Colab, Kaggle) were unsuccessful. These environments, while convenient, presented two major blockers:

1. **Resource Constraints:** The FP16 conversion process is memory-intensive and consistently caused crashes due to RAM limitations.
2. **Dependency Conflicts:** The pre-configured nature of notebook environments led to dependency conflicts with the specific versions required by the llama.cpp toolchain.

**Final Decision (The "Why"):**  
To overcome these issues and mitigate all technical risks, we made the strategic decision to use a dedicated, clean Google Cloud Platform (GCP) Virtual Machine. This approach provided full control over the environment, guaranteed access to the necessary CPU and RAM resources, and ultimately enabled the successful and reproducible creation of our model asset.

## 2. Environment Requirements

This process was successfully executed on a GCP instance with the following specifications:

- **OS:** Ubuntu 24.04 LTS (Noble Numbat)
- **CPU:** 8+ cores
- **RAM:** 32GB
- **Storage:** 200GB SSD

> 💡 **Note:** While GCP is used in this guide, any cloud provider or local machine that meets these specifications is suitable. Sufficient RAM (16GB+ minimum) is the most critical requirement.

## 3. Step-by-Step Conversion Process

The following commands represent the verified pipeline for creating the quantized model asset.

### Step 3.1: VM Setup and Dependencies

This prepares the virtual machine and installs all necessary tools and Python packages.

```bash
# Connect to GCP instance
gcloud compute ssh [YOUR_VM_NAME] --zone [YOUR_VM_ZONE]

# Install minimal system dependencies needed for virtual environment
sudo apt update && sudo apt install -y python3.12-venv

# Create and activate virtual environment before any other installations
python3 -m venv krishi_env
source krishi_env/bin/activate

# Now install remaining system dependencies
sudo apt install -y build-essential git python3-pip cmake

# Upgrade pip and install Python packages
pip install --upgrade pip
pip install transformers torch numpy sentencepiece protobuf accelerate safetensors
```

### Step 3.2: Authentication

Log in to your Hugging Face account to gain access to the gated Gemma model repository.

```bash
# Login to Hugging Face
huggingface-cli login
```

### Step 3.3: Build llama.cpp

Install additional system dependencies required for llama.cpp:

```bash
# Update package lists and install required libraries
sudo apt update
sudo apt install -y libcurl4-openssl-dev

# Clone llama.cpp repository and compile the necessary C++ tools
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
mkdir build && cd build
cmake ..
make -j$(nproc)
```

### Step 3.4: Model Download and Quantization

This two-stage process first downloads the model, then converts it to an intermediate FP16 format, and finally quantizes it to the production Q4_K_M format.

```bash
# Download the model
huggingface-cli download google/gemma-3n-E2B-it --local-dir gemma-model --exclude "*.gguf"

# Convert to GGUF format
python3 ../convert_hf_to_gguf.py gemma-model \
  --outfile gemma-model/gemma-3n-fp16.gguf \
  --outtype f16

# Quantize the model (Note: executables are in bin directory)
./bin/llama-quantize \
  gemma-model/gemma-3n-fp16.gguf \
  gemma-model/gemma-3n-q4_k_m.gguf \
  Q4_K_M
```

## 4. Visual Guide to Model Quantization

The following screenshots document the successful execution of the model quantization process:

### Step 1: Model Download and Conversion
![Model Conversion Process](images/1.png)
*Figure 1: Downloading the Gemma 3n model and converting it to GGUF format*

### Step 2: Quantization Execution
![Quantization Process](images/2.png)
*Figure 2: Running the quantization process with Q4_K_M settings*

### Step 3: Successful Completion
![Quantization Complete](images/3.png)
*Figure 3: Successful completion of model quantization*

## 5. Verification and Next Steps

After the pipeline completes, it is critical to verify the output and proceed with formal evaluation.

### Step 5.1: Verify Final Asset

Check the final file size to ensure the quantization was successful.

```bash
# Check final model size
ls -lh gemma-model/gemma-3n-q4_k_m.gguf
```

**Expected output:** The file size should be approximately 2.65 GB (reduced from the original 8.5GB FP16 version).

### Step 5.2: Performance Benchmarking

The final step before integration is to perform a rigorous benchmark of the Q4_K_M model against the FP16 baseline to quantify the trade-offs in performance and quality.

```bash
# Example test command (Note: executables are in bin directory)
./bin/llama-cli -m gemma-model/gemma-3n-q4_k_m.gguf -p "Hello, how are you?"
```

### Benchmark Visualizations

The following visualizations provide empirical evidence of the quantization's effectiveness:

#### 1. File Size Comparison
![File Size Comparison](images/file_size_comparison.png)
*Figure 1: 3.1x reduction in model size with Q4_K_M quantization*

#### 2. Inference Speed Comparison
![Inference Speed](images/inference_speed_comparison.png)
*Figure 2: Minimal impact on inference speed (32.10 vs 31.71 tokens/second)*

#### 3. Total Time Comparison
![Total Time](images/total_time_comparison.png)
*Figure 3: Negligible increase in total inference time*

### Detailed Benchmark Results

#### Performance Metrics

1. **Inference Speed (Tokens/Second)**
   ![Inference Speed 1](images/1.png)
   *Figure 4: Detailed inference speed comparison*

2. **Memory Usage**
   ![Memory Usage](images/2.png)
   *Figure 5: Memory consumption metrics*

3. **GPU Utilization**
   ![GPU Utilization](images/3.png)
   *Figure 6: GPU resource usage comparison*

4. **CPU Utilization**
   ![CPU Utilization](images/4.png)
   *Figure 7: CPU usage patterns*

#### Resource Efficiency

5. **VRAM Usage**
   ![VRAM Usage](images/5.png)
   *Figure 8: Video memory consumption*

6. **Power Consumption**
   ![Power Usage](images/6.png)
   *Figure 9: Power efficiency metrics*

7. **Latency Comparison**
   ![Latency](images/7.png)
   *Figure 10: Response time analysis*

8. **Throughput Analysis**
   ![Throughput](images/8.png)
   *Figure 11: Request handling capacity*

### Key Findings Summary

1. **Storage Efficiency**: 3.1x reduction in model size (8.11GB → 2.6GB)
2. **Performance Preservation**: Only 1.2% decrease in inference speed
3. **Optimal Trade-off**: Significant storage savings with negligible impact on performance
4. **Resource Efficiency**: Improved memory and power efficiency across all metrics

> **Note:** The complete results of our validation are documented in the project's official Model Card.

## 6. Key Corrections from Previous Version

- **Build Command:** Changed from `cmake --build . --config Release -j$(nproc)` to `make -j$(nproc)`
- **Executable Location:** All llama.cpp executables are located in the `bin/` directory, not the root build directory
- **File Size Expectation:** Corrected expected output size from 5-6GB to 2.65GB based on actual Q4_K_M quantization results
- **Version Update:** Updated to reflect July 10, 2025 corrections

---
*Last updated: July 10, 2025*