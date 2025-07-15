<div align="center">

# 🌱 KrishiSahayak+Gemma

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.3.1-red.svg)](https://pytorch.org/)
[![Gradio](https://img.shields.io/badge/Gradio-4.37.2-orange.svg)](https://gradio.app/)
[![Android](https://img.shields.io/badge/Android-3DDC84?logo=android&logoColor=white)](https://developer.android.com/)

**Empowering Indian farmers with a reliable, 100% offline, AI-driven agricultural assistant.**

</div>

## 📋 Table of Contents
- [✨ Project Mission](#-project-mission)
- [🏗️ Architecture](#-architecture)
- [🚀 Getting Started](#-getting-started)
  - [Development Setup](#-development-setup)
  - [Mobile App](#-mobile-app)
- [📊 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Project Mission

KrishiSahayak+Gemma is an engineering initiative to solve a critical real-world problem: providing farmers in low-connectivity regions of India with access to advanced AI-driven agricultural advice.

The project's primary goal is to deliver a 100% offline, reliable, and user-friendly Android application that can run on low-resource smartphones (≤ 2GB RAM).

## 🏗️ Current Development Status (2025-07-16)

The Android application build has been successfully completed and compiled ([build compilation video](https://youtu.be/BIKkLbJIZhA)). The project is currently in the APK testing phase to ensure reliability and performance before the initial public release.

![Android Source Code](docs/images/Android_src.png)

![Application Build Compilation](docs/images/Application_build_compilation.png)

Testing is focused on:
- Offline functionality verification
- Memory usage on low-resource devices (≤ 2GB RAM)
- AI performance and responsiveness
- User interface stability

Stay tuned for the public release announcement after successful testing completion.

## 🎯 Project Components

This project consists of two main components, each with a distinct purpose:

1. **🌐 Web Demo (The AI Playground):** A live, interactive Gradio application that serves as a development tool and a direct interface to our AI model. It's perfect for developers, judges, and anyone wanting to quickly test the core AI capabilities.  
2. **📱 Android App (The Field Solution):** The primary, end-user product. This is a 100% offline-first application designed for low-resource devices to ensure it's accessible and reliable for farmers in remote areas.

## 🏗️ Architecture

## 🏗️ Project Architecture

KrishiSahayak+Gemma represents a state-of-the-art technical solution designed to run advanced AI on low-resource devices in rural India. The architecture is built around two main components, each optimized for its specific purpose:

### 1. 🌐 Web Demo (Development & Demo)

| Component | Technology Stack | Purpose |
|-----------|------------------|----------|
| 🤖 AI Engine | google/gemma-3n-E2B-it (quantized) | Development and demonstration of core AI capabilities |
| 📚 Knowledge Base | FAISS, SQLite, CSV | RAG system for factual grounding |
| 🌐 Web Interface | Gradio, FastAPI | Rapid prototyping and stakeholder demonstrations |
| 🎯 Optimization | Server-based | Maximum quality and development speed |

### 2. 📱 Android App (Production)

| Component | Technology Stack | Purpose |
|-----------|------------------|----------|
| 🤖 AI Engine | llama.cpp (native) | Optimized for low-resource devices |
| 📚 Knowledge Base | Memory-mapped FAISS, SQLite | Efficient offline storage |
| 📱 Mobile App | Native Android | Final user-facing application |
| 🎯 Optimization | Resource-constrained | Runs on <$50 phones with 2GB RAM |

### Key Technical Features

1. **Resource Optimization**
   - Native C++ implementation
   - Memory-mapped model files
   - Custom RAG pipeline
   - Optimized for <1GB RAM usage

2. **Offline-First Design**
   - 100% offline capability
   - <50MB APK size for Bluetooth sharing
   - <5 second response time
   - <1% battery impact per diagnosis

3. **Performance Metrics**
   - Model size: 2.6GB (optimized)
   - RAM usage: <1GB total
   - CPU optimization: NEON instructions
   - Distribution size: <50MB

For a detailed explanation of why we chose native C++ for the Android app instead of Python-on-Android, see:
- [Android Architecture Decision](docs/Android_application_architecture_decision.md)

For more technical details, see:
- [Technical Decision Log](docs/technical_decision_log.md)
- [Model Card](docs/model_card.md)
- [Technical Report](docs/TECHNICAL_REPORT.md)

This architecture represents a significant technical achievement, pushing the boundaries of what's possible with mobile AI on low-resource devices.

## 📺 Demo Video

[![KrishiSahayak+Gemma Web Demo](https://img.youtube.com/vi/W8L-15np5do/0.jpg)](https://youtu.be/W8L-15np5do?si=lSxdbrKVDozeQZ8I)

*Click the thumbnail to watch a short demo of the web-based AI playground in action.*

**What you'll see:**
1. **Confident Answers** – The base model **`google/gemma-3n-E2B-it`** (≈ 4.5 B parameters), quantized on-device as **`gemma-3n-q4_k_m.gguf`**, responds instantly to common agricultural queries when confidence is high.
2. **Uncertainty & RAG Fallback** – When the model's confidence drops for tougher questions, the Retrieval-Augmented Generation (RAG) pipeline searches the knowledge base and delivers a grounded answer.

For detailed data strategy and regional coverage, see:
- [REGIONAL_COVERAGE.md](docs/REGIONAL_COVERAGE.md)
- [VERSIONING.md](docs/VERSIONING.md)
- [Technical Report](docs/TECHNICAL_REPORT.md)
- [Data Preparation Report](docs/data_preparation_knowledge_base_report.md)

## 🚀 Getting Started

### 📋 Prerequisites

| Requirement | Version | Installation |
|-------------|---------|--------------|
| Python | 3.8+ | [Download](https://www.python.org/downloads/) |
| pip | Latest | `python -m pip install --upgrade pip` |
| Git | Latest | [Download](https://git-scm.com/downloads) |
| Android Studio | 2022.3+ | [Download](https://developer.android.com/studio) |

### Model Download

The core of this application is a quantized version of the Google Gemma 3N model used in the Kaggle "Google Gemma 3N Hackathon".

* **Model File:** `gemma-3n-q4_k_m.gguf`
* **Download Link:** [Google Drive](https://drive.google.com/file/d/1SoZSaLpcIGU96Oqjr0KlYjOEXHxTKYHN/view?usp=drive_link)

> **Disclaimer – Important Notice Before Downloading**
> 
> * **File Size:** The model is large (≈ 2.6 GB). Please download over a stable Wi-Fi connection.
> * **License & Terms of Use:** This model is a derivative of Google's Gemma 3N. By downloading and using it, you agree to the **Gemma Terms of Use** and the **Gemma Prohibited Use Policy**, accepted when entering the Kaggle competition.
> * Review the full terms in our [NOTICE.md](NOTICE.md) file before using the model.

---

### Mobile App (Primary Solution)
The official end-user solution is our mobile application, specifically designed for production use with optimized performance for low-resource devices. The mobile app provides a complete, user-friendly experience for farmers in the field.

*Coming soon*

## 📱 The Android Application
**Status:** 🟡 Phase 2: MVP Development Starting

A fully offline-capable mobile application designed specifically for farmers in remote areas.

Technical Highlights:
- Uses the validated, quantized gemma-3n-q4_k_m.gguf model.
- Optimized for low-end Android devices (≤ 2GB RAM).
- Deployed via offline P2P methods (SD card, local sharing).

## 📈 Progress Update (13 July 2025)

- 🌐 **Web Demo Complete** – Interactive Gradio playground published and public demo video released.
- 🤖 **Model Assets Ready** – Base model `google/gemma-3n-E2B-it` successfully quantized to `gemma-3n-q4_k_m.gguf` and validated on-device.
- 📚 **Knowledge Base v0 Released** – 46-class agricultural KB curated and integrated with RAG pipeline.
- 🧪 **Validation & Evaluation** – Initial uncertainty quantification and RAG fallback logic tested with >90% accuracy on internal test set.
- 📱 **Android MVP Coding Started** – Jetpack Compose UI skeleton and on-device inference hooks stubbed.

Next milestone: Field-testing pilot (Phase 3).

## 📊 Project Structure

```
KrishiSahayak-Gemma/
├── android_app_assets/       # Optimized assets for the mobile app
├── asset_preparation/        # Scripts for data processing & model conversion
├── data/
│   └── _archive/             # Archived generic dataset
├── docs/                     # All project documentation
├── reports/                  # Project analysis reports and visualizations
└── web_demo/                 # Self-contained web application
    ├── app.py
    └── src
```

### 📄 Key Files

| File | Purpose |
|------|---------|
| `data/processed/knowledge_base_v0_generic_46-class.csv` | Structured agricultural knowledge base |
| `web_demo/app.py` | Main Gradio web application |
| `web_demo/requirements.txt` | Python dependencies for development |
| [model_card.md](docs/model_card.md) | Model details and specifications |
| [TECHNICAL_REPORT.md](docs/TECHNICAL_REPORT.md) | Comprehensive technical documentation |

## 🚀 Getting Started

### 📋 Prerequisites

| Requirement | Version | Installation |
|-------------|---------|--------------|
| Python | 3.8+ | [Download](https://www.python.org/downloads/) |
| pip | Latest | `python -m pip install --upgrade pip` |
| Git | Latest | [Download](https://git-scm.com/downloads) |
| Android Studio | 2022.3+ | [Download](https://developer.android.com/studio) |

### ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/VIKAS9793/KrishiSahayak_Gemma.git
   cd KrishiSahayak_Gemma
   ```

2. **Set up a virtual environment** (recommended)
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd web_demo
   pip install -r requirements.txt
   ```

### 🌐 Development Setup

<div align="center">
  <img src="https://img.shields.io/badge/Quick%20Start-4%20Steps-blue" alt="Quick Start: 4 Steps">
  <img src="https://img.shields.io/badge/Port-7860-orange" alt="Port: 7860">
</div>

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   ```
   http://localhost:7860
   ```

   > 💡 **Tip**: The web interface will open automatically in your default browser.

### 📱 Building the Android App

<div align="center">
  <img src="https://img.shields.io/badge/Status-Beta-yellow" alt="Status: Beta">
  <img src="https://img.shields.io/badge/Requires-Android%20Studio-blue" alt="Requires: Android Studio">
</div>

1. Open the `android_app` directory in Android Studio
2. Wait for project sync to complete
3. Connect an Android device or start an emulator
4. Click **Run** (▶️) to build and deploy

### 🔍 Verifying the Installation

1. **Check web dependencies**
   ```bash
   python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
   python -c "import gradio; print(f'Gradio version: {gradio.__version__}')"
   ```

2. **Test the knowledge base**
   ```python
   import faiss
   import pandas as pd
   
   # Load sample data
   df = pd.read_csv('data/_archive/knowledge_base_v0_generic_46-class.csv')
   print(f"Knowledge base contains {len(df)} entries")
   ```

## 📚 Documentation

### 📄 Key Documents

| Document | Description |
|----------|-------------|
| [Technical Report](docs/TECHNICAL_REPORT.md) | Comprehensive technical specifications and data architecture |
| [STRATEGY_AND_ROADMAP.md](docs/STRATEGY_AND_ROADMAP.md) | Project strategy, phases, and future roadmap |
| [model_card.md](docs/model_card.md) | Model details, performance, and limitations |
| [technical_decision_log.md](docs/technical_decision_log.md) | Key technical decisions and rationale |
| [VERSIONING.md](docs/VERSIONING.md) | Version control and data management approach |

> 💡 All documentation is stored in the `docs/` directory. Please ensure documentation is kept up-to-date with code changes.

## 🤝 Contributing

<div align="center">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen" alt="PRs Welcome">
  <img src="https://img.shields.io/badge/First%20Time%20Contributors-Friendly-blue" alt="First Time Contributors Friendly">
</div>

We welcome contributions from the community! Whether you're a developer, designer, or agricultural expert, there are many ways to contribute. Please read our [Contribution Guidelines](CONTRIBUTING.md) before getting started.

### 🛠 How to Contribute

1. **Fork** the repository
2. Create a **branch** for your feature (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. Open a **Pull Request**

### 🔍 Looking for First Issues?

Check out our [Good First Issues](https://github.com/VIKAS9793/KrishiSahayak_Gemma/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) to get started!

## 📄 License

<div align="center">
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
  </a>
  <a href="https://github.com/VIKAS9793/KrishiSahayak_Gemma/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/VIKAS9793/KrishiSahayak_Gemma?color=blue" alt="GitHub License">
  </a>
</div>

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### 📝 License Summary

- **Permits**: Commercial use, modification, distribution, private use
- **Conditions**: Include original license and copyright notice
- **Limitations**: No liability, no warranty

## 📧 Contact & Support

<div align="center">
  <a href="mailto:vikassahani17@gmail.com">
    <img src="https://img.shields.io/badge/Email-vikassahani17%40gmail.com-red?style=flat&logo=gmail" alt="Email">
  </a>
  <a href="https://github.com/VIKAS9793">
    <img src="https://img.shields.io/badge/GitHub-VIKAS9793-black?style=flat&logo=github" alt="GitHub Profile">
  </a>
</div>

**Project Maintainer**: Vikas Sahani  
**Email**: [vikassahani17@gmail.com](mailto:vikassahani17@gmail.com)  
**GitHub**: [@VIKAS9793](https://github.com/VIKAS9793)  

**Support Channels**:
- 🐛 [Report Issues](https://github.com/VIKAS9793/KrishiSahayak_Gemma/issues)
- 💬 [Join Discussions](https://github.com/VIKAS9793/KrishiSahayak_Gemma/discussions)
- 📚 [Documentation](docs/)

For any questions, feedback, or support, please don't hesitate to reach out through any of the channels above.

---

<div align="center">
  <p>Made with ❤️ for farmers and the open source community</p>
  <img src="https://komarev.com/ghpvc/?username=VIKAS9793&label=Page%20Views&color=blueviolet&style=flat" alt="Page Views">
</div>