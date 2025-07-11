# KrishiSahayak+Gemma Web Demo - Deployment Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Detailed Setup](#detailed-setup)
4. [Troubleshooting](#troubleshooting)
5. [Common Issues](#common-issues)

## System Requirements

### Minimum Requirements
- **OS**: Ubuntu 20.04/22.04 LTS (recommended), Windows 10/11, or macOS
- **CPU**: 4+ cores (8+ recommended)
- **RAM**: 16GB+ (32GB recommended)
- **Storage**: 50GB+ free space (SSD recommended)
- **Python**: 3.8 or higher
- **Git**
- **FFmpeg**: Required for audio processing
- **Build Tools**: Required for compiling some dependencies

### Recommended for Production
- **GPU**: NVIDIA GPU with 8GB+ VRAM (for faster inference)
- **RAM**: 32GB+
- **Storage**: 100GB+ SSD

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/VIKAS9793/KrishiSahayak_Gemma.git
cd KrishiSahayak_Gemma/web_demo
```

### 2. Set Up Environment
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install system dependencies (Ubuntu/Debian)
sudo apt update && sudo apt install -y \
    python3-pip \
    python3-venv \
    ffmpeg \
    build-essential

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install FAISS (CPU version)
pip install faiss-cpu

# (Optional) For development
pip install -r requirements-dev.txt
```

### 3. Download Models
```bash
# Create model directory
mkdir -p model

# Download the quantized Gemma model (gemma-3n-q4_k_m.gguf)
# Example:
# wget -O model/gemma-3n-q4_k_m.gguf "YOUR_MODEL_DOWNLOAD_URL"
```

### 4. Obtain the Model
Before running the application, you'll need to obtain the `gemma-3n-q4_k_m.gguf` model file. This model is a quantized version of Google's Gemma 3B model, specifically optimized for this application.

#### Option 1: Download from Source
```bash
# Create model directory if it doesn't exist
mkdir -p model

# Download the model (replace URL with actual source)
wget -O model/gemma-3n-q4_k_m.gguf "YOUR_MODEL_DOWNLOAD_URL"
```

#### Option 2: Convert from Base Model
If you have access to the base model, you can quantize it using the following steps:
```bash
# Install required tools
pip install auto-gptq

# Convert and quantize the model
python scripts/quantize.py --model-id google/gemma-3n-E2B-it --output model/gemma-3n-q4_k_m.gguf
```

### 5. Run the Application
```bash
python app.py
```

Access the web interface at: http://127.0.0.1:7860

## Monitoring and Logging

The application includes built-in monitoring and logging to help track performance and diagnose issues:

### Log Files
- Application logs are stored in `logs/app.log`
- Access logs are stored in `logs/access.log`

### Monitoring Endpoints
- Health check: `http://localhost:7860/health`
- Metrics: `http://localhost:7860/metrics`
- System status: `http://localhost:7860/status`

### Environment Variables for Logging
```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/app.log
LOG_FORMAT=json  # json or text
```

## Detailed Setup

### 1. Environment Variables
Create a `.env` file in the web_demo directory:
```env
# Required
MODEL_PATH=../model/gemma-3n-q4_k_m.gguf

# Optional
PORT=7860
LOG_LEVEL=INFO
```

### 2. Audio Setup
For audio processing, ensure:
- FFmpeg is installed
- Required audio codecs are available

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install -y ffmpeg
```

**Windows:**
- Download FFmpeg from https://ffmpeg.org/download.html
- Add FFmpeg to your system PATH

### 3. Knowledge Base Setup
```bash
# Ensure knowledge base files exist
ls data/processed/
# Should include:
# - knowledge_base_v0_generic_46-class.faiss
# - knowledge_base_v0_generic_46-class_text.pkl
```

## Troubleshooting

### Common Issues

#### 1. Model Loading Issues
**Error**: "Failed to load model"
- Verify the model file exists at the specified path
- Check file permissions (`chmod +x model/*`)
- Ensure sufficient disk space
- For GGUF models, verify the file is not corrupted

#### 2. Audio Processing Issues
**Error**: "ffmpeg not found" or "No such file or directory: 'ffmpeg'"
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y ffmpeg

# Verify installation
ffmpeg -version
```
- Add FFmpeg to system PATH if not detected

#### 3. Knowledge Base Loading Issues
**Error**: "Ran out of input" or missing knowledge base files
```bash
# Verify files exist
ls -lh data/processed/
# Should include:
# - knowledge_base_v0_generic_46-class.faiss
# - knowledge_base_v0_generic_46-class_text.pkl

# Regenerate if needed
cd ../asset_preparation
python build_index.py --input_csv ../data/processed/knowledge_base_v0_generic_46-class.csv --output_dir ../data/processed/
```

#### 4. Memory Issues
**Error**: "CUDA out of memory" or "Not enough memory"
- Reduce batch size in `app.py`
- Use CPU instead of GPU (slower but uses less memory)
- Close other memory-intensive applications
- For CPU usage, ensure sufficient swap space

#### 5. Dependency Conflicts
**Error**: Version conflicts during installation
```bash
# Create fresh virtual environment
python -m venv fresh_venv
source fresh_venv/bin/activate

# Install exact versions
pip install -r requirements.txt --no-cache-dir
```

#### 6. SQLite Database Issues
**Error**: "No such table" or database corruption
```bash
# Check database contents
sqlite3 data/processed/knowledge_base_v0_generic_46-class.sqlite ".tables"

# Export to CSV if needed
sqlite3 -header -csv data/processed/knowledge_base_v0_generic_46-class.sqlite "SELECT * FROM knowledge;" > knowledge_export.csv
```

#### 7. Missing Python Packages
**Error**: "ModuleNotFoundError"
- Verify all packages in requirements.txt are installed
- Check for case sensitivity in imports
- Try reinstalling problematic packages with `--force-reinstall`

#### 8. File Permission Issues
**Error**: "Permission denied"
```bash
# Fix directory permissions
chmod -R 755 data/
chmod -R 755 model/

# Fix file ownership if needed
sudo chown -R $USER:$USER ./
```

### Logs
Check logs in the terminal where you ran `app.py` for detailed error messages.

## Advanced Configuration

### Running on a Different Port
```bash
python app.py --port 8080
```

### Enabling Debug Mode
```bash
python app.py --debug
```

### Running with GPU Acceleration
Ensure CUDA is properly installed, then run:
```bash
python app.py --device cuda
```

## Support
For additional help, please open an issue on our GitHub repository.

---
Last Updated: July 2024
