# Contributing to KrishiSahayak+Gemma

First off, thank you for considering contributing to the KrishiSahayak project! Your help is essential for our mission to empower farmers with accessible AI technology.

This document provides guidelines for contributing to the project. We welcome contributions of all kinds, from bug reports and feature suggestions to documentation improvements and code pull requests.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How You Can Contribute

There are many ways to contribute to the project's success:

- **Reporting Bugs**: If you find a bug or have an issue with the setup, please open an issue and provide as much detail as possible.
- **Suggesting Enhancements**: Have an idea for a new feature or an improvement to an existing one? We'd love to hear it! Please open an issue to start a discussion.
- **Improving Documentation**: If you find parts of our documentation unclear or inaccurate, please let us know or submit a pull request with your improvements.
- **Submitting Pull Requests**: If you have a bug fix or a new feature you'd like to contribute, please follow the process outlined below.

## A Special Call for Domain Experts

A core part of our long-term vision is building high-quality, expert-verified Regional Data Packs. If you are an agricultural scientist, researcher, agronomist, or botanist, your expertise is invaluable. We are actively seeking collaborators to help us curate and validate the data that will power our application. Please reach out to the project maintainers if you are interested in contributing in this capacity.

## Setting Up Your Development Environment

To get started with the code, follow these steps. This guide focuses on setting up the web_demo.

### Fork & Clone the Repository

1. [Fork the repository](https://github.com/VIKAS9793/KrishiSahayak_Gemma/fork) on GitHub.
2. Clone your fork to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/KrishiSahayak_Gemma.git
   cd KrishiSahayak_Gemma
   ```

### Create and Activate a Virtual Environment (Crucial Step)

It is essential to use a Python virtual environment to avoid conflicts with system-wide packages.

From the project root directory, run:

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the environment
# On Windows:
# .\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Install Dependencies

Dependencies are managed in the project root. Install them using pip:

```bash
pip install -r requirements.txt
```

## Submitting Changes (Pull Request Process)

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. Make your changes and commit them with a clear, descriptive message.
3. Push your branch to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```
4. Open a Pull Request from your fork's branch to the main branch of the original repository.
5. Clearly describe the changes you have made and link to any relevant issues.
6. The project maintainers will review your PR, provide feedback, and merge it when it's ready.

## Style Guides

- **Python**: Please follow the [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/). We recommend using an autoformatter like `black` to ensure consistency.
- **Documentation**: All documentation is written in Markdown. Please ensure it is clear, concise, and easy to read.

Thank you again for your interest in contributing!
