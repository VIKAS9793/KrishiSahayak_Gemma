# --- src/pipeline/inference.py (Final Version) ---
# This version uses llama-cpp-python to run the GGUF model on a CPU.
# It is highly efficient and does not require a GPU.

from llama_cpp import Llama
from PIL import Image
import os

# --- Configuration ---
# Point this to the location of your GGUF model file.
MODEL_PATH = os.path.join(
    os.path.dirname(__file__), '..', '..', 'model', 'gemma-3n-q4_k_m.gguf'
)

# --- Model Loading (with caching) ---
model = None

def load_model():
    """
    Loads the GGUF model using llama-cpp-python.
    """
    global model
    if model is None:
        print(f"Loading GGUF model from: {MODEL_PATH}")
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at {MODEL_PATH}. "
                "Please ensure you have downloaded the gemma-3n-q4_k_m.gguf file "
                "and placed it in the web_demo/model/ directory."
            )
        try:
            # Note: For multimodal models, llama-cpp-python requires a special
            # "clip_model_path" to handle the image part. We will simulate
            # text-only input for this local demo to keep it simple.
            model = Llama(
                model_path=MODEL_PATH,
                n_ctx=2048,  # Context size
                n_threads=max(os.cpu_count() - 1, 1), # Use all cores but one
                verbose=False # Set to True for more detailed logs
            )
            print("✅ GGUF model loaded successfully via llama-cpp-python.")
        except Exception as e:
            print(f"❌ Error loading GGUF model: {e}")
            raise

def get_gemma_diagnosis(image_path: str, user_query: str) -> str:
    """
    Generates a diagnosis for a given user query.
    NOTE: This simplified version for local demo ignores the image and uses text only.
    """
    if model is None:
        load_model()
    
    try:
        # Build a prompt suitable for a text-only query
        prompt = (
            f"<start_of_turn>user\n"
            f"A farmer is showing a plant leaf and asks: '{user_query}'. "
            f"Based on this, what is the likely issue and what is the remedy?"
            f"<end_of_turn>\n<start_of_turn>model\n"
        )

        # Generate the response
        output = model(
            prompt,
            max_tokens=256,
            stop=["<end_of_turn>"],
            temperature=0.3,
            echo=False
        )
        
        response_text = output['choices'][0]['text'].strip()
        return response_text
    except Exception as e:
        print(f"❌ Error during inference: {e}")
        return "Error during inference."

