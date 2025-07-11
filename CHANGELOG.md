# Changelog

All notable changes to the KrishiSahayak+Gemma project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.10.0] - 2025-07-08
### Added
- Initial public release of KrishiSahayak+Gemma
- Core functionality for agricultural disease diagnosis
- Core AI pipeline with image and audio processing support
- Documentation for model conversion and data preparation
- Pre-processed knowledge base for 46 plant-disease classes
- Model quantization scripts and guides
- API endpoints for model inference
- Basic authentication and rate limiting

### Technical Details
- Uses Gemma 3n model with 4-bit quantization
- Implements RAG (Retrieval-Augmented Generation)
- Supports multiple regional languages
- Offline-first architecture

### Known Issues
- Limited to 46 plant-disease classes in initial release
- Performance may vary with regional variations
- Mobile app integration in development
