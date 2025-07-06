# Model Card: KrishiSahayak Web Demo

## Model Details
- **Base Model:** `google/gemma-3n-E2B-it`
- **Format:** Hugging Face `safetensors`
- **Inference Library:** `transformers`
- **Quantization:** `BitsAndBytes` (on-the-fly 4-bit)
- **Purpose:** This model powers the server-side inference for the web demo. This model is **not** the final mobile asset.

## Intended Use
This model is designed for demonstration and testing purposes as part of the KrishiSahayak web interface. It provides diagnostic capabilities for crop health based on multimodal inputs.

## Performance

### Hardware
- **CPU:** 8+ cores recommended
- **RAM:** 16GB+ recommended
- **GPU:** Not required but recommended for faster inference

### Inference Speed
- **Initial Load Time:** ~10-15 seconds
- **Average Response Time:** 2-5 seconds per query (varies by input complexity)

## Dependencies
- Python 3.9+
- PyTorch 2.0+
- Transformers 4.30+
- BitsAndBytes 0.40.0+
- Accelerate 0.20.0+

## Limitations
- This is a server-side model requiring internet connectivity
- Not optimized for low-resource environments
- May have higher latency than the mobile-optimized version

## Ethical Considerations
This model is intended for demonstration purposes only. For production use, especially in agricultural settings, please ensure:
- Proper validation of model outputs
- Human oversight of critical decisions
- Consideration of local agricultural practices and conditions

## Contact
For questions about this model, please contact:
- **Vikas Sahani**
  - Email: [vikassahani17@gmail.com](mailto:vikassahani17@gmail.com)
  - LinkedIn: [Vikas Sahani](https://www.linkedin.com/in/vikas-sahani-727420358)

Or refer to the main project documentation.
