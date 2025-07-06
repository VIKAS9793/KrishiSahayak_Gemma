# Gemma Model Conversion and Quantization Guide

This guide documents the process of converting and quantizing the Google Gemma 3n model for deployment in the Krishi Sahayak application.

## Purpose
This guide provides step-by-step instructions for preparing the Gemma model for mobile deployment, including:
- Setting up the development environment
- Converting the model to GGUF format
- Quantizing the model for efficient mobile inference
- Verifying the model's functionality

## Prerequisites
- Google Cloud Platform account with VM access (or any cloud provider)
- Hugging Face account with access token
- Access to the gated Gemma model repository

## Environment Requirements

### Minimum Requirements
- **CPU**: 8 cores
- **RAM**: 16GB
- **Storage**: 200GB SSD (recommended)
- **OS**: Ubuntu 24.04 LTS (Noble Numbat) - 64-bit server/minimal installation

### Recommended Setup
- **CPU**: 8+ cores
- **RAM**: 32GB+ for smoother operation
- **Storage**: 200GB+ NVMe SSD for better I/O performance
- **Swap Space**: 8GB (if using minimum RAM configuration)

> 💡 **Note**: While GCP is used in this guide, you can use any cloud provider or local machine that meets these specifications. The key requirements are sufficient compute power and memory to handle the model conversion process efficiently.

## Model Conversion Process

### 1. VM Setup and Dependencies
```bash
# Connect to GCP instance
gcloud compute ssh [YOUR_VM_NAME] --zone [YOUR_VM_ZONE]

# Install system dependencies
sudo apt update && sudo apt install -y build-essential git python3-pip cmake

# Install Python packages
pip3 install transformers torch numpy sentencepiece protobuf accelerate safetensors
```

### 2. Authentication
```bash
# Login to Hugging Face
huggingface-cli login
```

### 3. Build llama.cpp
```bash
git clone https://github.com/ggerganov/llama.cpp.git
cd llama.cpp
mkdir build && cd build
cmake ..
cmake --build . --config Release -j$(nproc)
```

### 4. Model Download and Conversion
```bash
# Download the model
huggingface-cli download google/gemma-3n-E2B-it --local-dir gemma-model --exclude "*.gguf"

# Convert to GGUF format
python3 ../convert_hf_to_gguf.py gemma-model \
  --outfile gemma-model/gemma-3n-fp16.gguf \
  --outtype f16

# Quantize the model
./llama-quantize \
  gemma-model/gemma-3n-fp16.gguf \
  gemma-model/gemma-3n-q4_k_m.gguf \
  Q4_K_M
```

### 5. Verify and Test
```bash
# Check final model size
ls -lh gemma-model/gemma-3n-q4_k_m.gguf

# Test the model
./llama-cli -m gemma-model/gemma-3n-q4_k_m.gguf -p "Hello, how are you?"
```

## Model Specifications

| Stage | File Size | Description |
|-------|-----------|-------------|
| Original Download | ~11GB | Hugging Face safetensors |
| GGUF FP16 | 8.4GB | Intermediate format |
| **Final Q4_K_M** | **2.65GB** | **Deployment-ready model** |

## Integration Notes
- The final quantized model is optimized for Android deployment
- Model size is reduced by ~75% while maintaining good quality
- Ensure your application handles the ~2.65GB model file appropriately
- Consider progressive loading for better user experience

## Troubleshooting

### Common Issues
1. **Memory errors**: Ensure VM has sufficient RAM (16GB+ recommended)
2. **Build failures**: Verify all dependencies are installed
3. **Authentication issues**: Double-check Hugging Face access token

### Adding Swap Space (if needed)
```bash
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Next Steps
1. Integrate the model into the Android application
2. Implement appropriate model loading and inference logic
3. Test performance on target devices
4. Monitor memory usage and optimize as needed

## References
- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [Hugging Face Gemma](https://huggingface.co/google/gemma-3n-E2B-it)
- [Google Cloud Documentation](https://cloud.google.com/)

---
*Last updated: July 2025*
