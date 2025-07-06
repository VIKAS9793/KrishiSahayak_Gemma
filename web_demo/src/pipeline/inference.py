# --- src/pipeline/inference.py ---
# Version 3: Final version for local CPU execution.

import torch
from transformers import AutoProcessor, Gemma3nForConditionalGeneration, BitsAndBytesConfig
from PIL import Image
import os

# --- Configuration ---
MODEL_ID = "google/gemma-3n-e2b-it"

# --- Model Loading (with caching) ---
model = None
processor = None

def load_model():
    """
    Loads the Gemma 3n model and processor.
    This version is compatible with CPU-only machines.
    """
    global model, processor

    if model is None:
        print("Loading Gemma 3n model for the first time... (This may take a while on CPU)")
        
        try:
            # Determine the device and data type
            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.bfloat16 if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float32
            print(f"Using device: {device} with dtype: {dtype}")

            cache_dir = "./model_cache"
            
            # NOTE: We are NOT using 4-bit quantization here to ensure CPU compatibility.
            # This will use more RAM but will not require a GPU with CUDA.
            model = Gemma3nForConditionalGeneration.from_pretrained(
                MODEL_ID,
                torch_dtype=dtype,
                cache_dir=cache_dir
            ).to(device) # Move model to the selected device
            
            processor = AutoProcessor.from_pretrained(MODEL_ID, cache_dir=cache_dir)
            print("✅ Model and processor loaded successfully.")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise

def generate_text_from_prompt(prompt: str) -> str:
    """
    Generates text from a given text-only prompt.
    """
    if model is None or processor is None: load_model()
    try:
        inputs = processor(text=prompt, return_tensors="pt").to(model.device)
        generation_output = model.generate(**inputs, max_new_tokens=512, do_sample=True, temperature=0.7)
        response_text = processor.decode(generation_output[0], skip_special_tokens=True)
        return response_text.split("model\n")[-1].strip()
    except Exception as e:
        print(f"❌ Error during text generation: {e}"); return "Error during generation."

def get_gemma_diagnosis(image_path: str, user_query: str) -> str:
    """
    Generates a diagnosis for a given plant image and user query.
    """
    if model is None or processor is None: load_model()
    if not os.path.exists(image_path): return "Error: Image file not found."
    try:
        image = Image.open(image_path).convert("RGB")
        prompt = f"<image>\n<start_of_turn>user\n{user_query}<end_of_turn>\n<start_of_turn>model\n"
        inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)
        generation_output = model.generate(**inputs, max_new_tokens=250, do_sample=False)
        response_text = processor.decode(generation_output[0], skip_special_tokens=True)
        return response_text.split("model\n")[-1].strip()
    except Exception as e:
        print(f"❌ Error during inference: {e}"); return "Error during inference."
