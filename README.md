<div align="center">

# 🌱 KrishiSahayak+Gemma

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.3.1-red.svg)](https://pytorch.org/)
[![Gradio](https://img.shields.io/badge/Gradio-4.37.2-orange.svg)](https://gradio.app/)
[![Android](https://img.shields.io/badge/Android-3DDC84?logo=android&logoColor=white)](https://developer.android.com/)

**Empowering farmers with AI-driven agricultural assistance**

</div>

## 📋 Table of Contents
- [✨ Features](#-features)
- [🏗️ Architecture](#%EF%B8%8F-architecture)
- [🚀 Getting Started](#-getting-started)
- [🌐 Web Demo](#-web-demo)
- [📱 Mobile App](#-mobile-application)
- [📊 Project Structure](#-project-structure)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## ✨ Features

### 🌾 Core Capabilities
- **🌱 Plant Disease Diagnosis** - AI-powered image analysis for crop health
- **🔍 Knowledge Base** - Extensive agricultural database with offline access
- **🗣️ Multilingual Support** - Voice and text in regional languages
- **📱 Cross-Platform** - Web and mobile interfaces for all users

## 🏗️ Architecture

KrishiSahayak+Gemma is built with a modular, scalable architecture that supports both web and mobile platforms while sharing a common knowledge base and AI capabilities.

### 🧱 Core Components

| Component | Technology Stack | Purpose |
|-----------|------------------|---------|
| **AI Engine** | PyTorch, Transformers, Gemma | NLP, image processing, model inference |
| **Knowledge Base** | FAISS, SQLite, CSV | Agricultural data storage and retrieval |
| **Web Interface** | Gradio, FastAPI | User interaction and visualization |
| **Mobile App** | Android, SQLite | Offline-capable native application |
| **Data Processing** | Pandas, NumPy | Data transformation and preparation |

### 🔄 Data Flow

```mermaid
graph TD
    A[User Input] --> B{Input Type}
    B -->|Image| C[Image Processing]
    B -->|Audio| D[Speech-to-Text]
    B -->|Text| E[Query Processing]
    
    C --> F[AI Analysis]
    D --> E
    E --> F
    
    F --> G[Knowledge Base Search]
    G --> H[Response Generation]
    H --> I[User Interface]
    
    I --> J[Web App]
    I --> K[Mobile App]
```

### 🗃️ Data Storage

#### Global Knowledge Base
All dataset versions are stored in the `data/_archive/` directory with versioned filenames.

**Current Version (v0 - Generic 46-class Dataset)**
- `knowledge_base_v0_generic_46-class.csv` - Structured agricultural knowledge (46 classes)
- `knowledge_base_v0_generic_46-class.faiss` - Vector embeddings for semantic search
- `knowledge_base_v0_generic_46-class_text.pkl` - Pre-processed text data
- `knowledge_base_v0_generic_46-class.sqlite` - SQLite database for mobile

#### Regional Knowledge Bases
Our system includes specialized knowledge bases for all 36 states and union territories of India, ensuring locally relevant agricultural information.

**Coverage:**
- 28 states (e.g., Maharashtra, Punjab, Kerala)
- 8 union territories (e.g., Delhi, Jammu & Kashmir, Ladakh)

**Structure:**
```
regional_kbs/
├── 1_raw_text/        # Raw text data collection
├── 2_curated_csv/     # Processed and cleaned CSVs
├── 3_sqlite_packs/    # Mobile-optimized SQLite databases
└── 4_faiss_packs/     # FAISS indices for semantic search
```

Learn more about our [Regional Data Pack Architecture](docs/regional_data_pack_adr.md)

## 🌐 Web Demo

<div align="center">
  <img src="https://img.shields.io/badge/Status-Online-brightgreen" alt="Status: Online">
  <img src="https://img.shields.io/badge/Model-Gemma%203B-blue" alt="Model: Gemma 3B">
  <img src="https://img.shields.io/badge/API-FastAPI-green" alt="API: FastAPI">
</div>

**Status:** 🟢 Fully Functional

A feature-rich web application that demonstrates the core capabilities of our agricultural AI assistant. Perfect for testing and demonstration purposes.

### Key Features:
- 🌿 Plant disease diagnosis from images
- 🎤 Voice query support in multiple languages
- 📝 Detailed diagnostic reports with remedies
- 🎧 Audio responses in regional languages
- 🔍 Knowledge base integration for accurate information

### Quick Start:
```bash
# Navigate to web_demo directory
cd web_demo

# Install dependencies
pip install -r requirements.txt

# Launch the application
python app.py
```

*For detailed setup instructions, see the [Web Demo Documentation](web_demo/README.md).*

## 📱 Mobile Application

<div align="center">
  <img src="https://img.shields.io/badge/Status-Development-yellow" alt="Status: Development">
  <img src="https://img.shields.io/badge/Platform-Android-green" alt="Platform: Android">
  <img src="https://img.shields.io/badge/Storage-SQLite-blue" alt="Storage: SQLite">
</div>

**Status:** 🟡 In Development (MVP Phase)

A fully offline-capable mobile application designed specifically for farmers in remote areas with limited or no internet connectivity.

### Planned Features:
- 📶 100% offline functionality
- 🌍 Local language support
- 🔋 Low-resource operation
- 📊 Crop health monitoring
- 📅 Agricultural calendar
- 💡 Expert farming tips

### 🛠 Technical Highlights:
- Uses quantized `gemma-3n-q4_k_m.gguf` model
- Optimized for low-end Android devices
- Minimal storage and memory footprint
- Regular offline knowledge base updates

### Development Progress:
- [x] Core AI model integration
- [x] Basic UI/UX implementation
- [ ] Local database setup
- [ ] Offline knowledge base
- [ ] Field testing

## 📊 Project Structure

```
KrishiSahayak-Gemma/
├── android_app/              # Android application source
│   └── src/main/assets/
│       └── knowledge_base_v0_generic_46-class.sqlite
│
├── asset_preparation/        # Data processing scripts
│   ├── build_index.py
│   ├── create_database.py
│   └── generate_knowledge_base_gemma.py
│
├── data/                     # Data storage
│   ├── _archive/            # Archived dataset versions
│   ├── knowledge_base_text.pkl
│   ├── processed/           # Processed datasets
│   ├── raw/                 # Raw data files
│   └── regional_kbs/        # Regional knowledge bases
│       ├── 1_raw_text/
│       ├── 2_curated_csv/
│       ├── 3_sqlite_packs/
│       └── 4_faiss_packs/
│
├── docs/                     # Project documentation
│   ├── TECHNICAL_REPORT.md
│   ├── technical_decision_log.md
│   ├── regional_data_pack_adr.md
│   ├── VERSIONING.md
│   └── DEV_LOGS.md
│
├── reports/                  # Analysis and performance reports
│   ├── eda_results/
│   └── validation_results/
│
└── web_demo/                 # Web-based demonstration
    ├── app.py
    ├── requirements.txt
    ├── MODEL_CARD.md
    └── src/
        ├── pipeline/
        ├── rag/
        └── utils/
```

### 📄 Key Files

| File | Purpose |
|------|---------|
| `knowledge_base_v0_generic_46-class.sqlite` | SQLite database for Android app (offline use) |
| `knowledge_base_v0_generic_46-class.faiss` | FAISS index for efficient similarity search |
| `knowledge_base_v0_generic_46-class.csv` | Structured agricultural knowledge base |
| `knowledge_base_v0_generic_46-class_text.pkl` | Pre-processed text data for RAG |
| `app.py` | Main Gradio web application |
| `requirements.txt` | Python dependencies for the web demo |

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

### 🌐 Running the Web Demo

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
| [Model Card](web_demo/MODEL_CARD.md) | Model details, performance, and limitations |
| [Technical Decision Log](docs/technical_decision_log.md) | Key technical decisions and rationale |
| [Development Logs](docs/DEV_LOGS.md) | Daily development updates and progress |

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
  <img src="https://komarev.com/ghpvc/?username=VIKAS9793&label=Project%20Visitors&color=blueviolet&style=flat" alt="Project Visitors">
</div>