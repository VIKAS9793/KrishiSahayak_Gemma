# evaluate.py
# A dedicated script for systematically testing the KrishiSahayak+Gemma pipeline.

import os
import sys
import json

# --- Setup System Path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# --- Import Core Logic ---
# We import a modified pipeline function to capture output instead of just printing it.
from main import run_full_pipeline, load_gemma_model, load_whisper_model, load_search_dependencies

# --- Test Case Configuration ---
EVALUATION_SET_DIR = "data/evaluation_set"

# Define our test cases. These correspond to the folder names in the evaluation directory.
TEST_CASES = [
    {
        "name": "Clear Image, Clear Query",
        "path": os.path.join(EVALUATION_SET_DIR, "test_case_1_clear"),
        "description": "Tests the pipeline's performance on a straightforward, high-quality input."
    },
    {
        "name": "Ambiguous Image, Vague Query",
        "path": os.path.join(EVALUATION_SET_DIR, "test_case_2_ambiguous"),
        "description": "Tests the RAG fallback mechanism with a challenging, low-quality input."
    },
    # We can add more test cases here as needed.
]

def setup_dummy_test_files():
    """Creates dummy files for the test cases if they don't exist."""
    from PIL import Image
    import numpy as np
    import scipy.io.wavfile as wav

    print("--- Checking for test assets... ---")
    for case in TEST_CASES:
        case_path = case["path"]
        image_path = os.path.join(case_path, "leaf_image.jpg")
        audio_path = os.path.join(case_path, "query.wav")

        if not os.path.exists(image_path):
            os.makedirs(case_path, exist_ok=True)
            print(f"Creating dummy image for '{case['name']}' at {image_path}")
            color = 'green' if 'clear' in case_path else 'brown'
            Image.new('RGB', (100, 100), color=color).save(image_path)
        
        if not os.path.exists(audio_path):
            os.makedirs(case_path, exist_ok=True)
            print(f"Creating dummy audio for '{case['name']}' at {audio_path}")
            # Create a short, silent wav file
            sample_rate = 44100
            duration = 1
            silence = np.zeros(int(duration * sample_rate))
            wav.write(audio_path, sample_rate, silence.astype(np.int16))
    print("--- Test asset check complete. Please replace dummy files with real test data. ---\n")


def run_evaluation():
    """
    Runs the full evaluation suite and prints a report.
    """
    print("="*60)
    print("          KrishiSahayak+Gemma Evaluation Suite")
    print("="*60)

    # --- 1. Initial Setup ---
    print("\n--- Initializing all models... ---")
    try:
        load_gemma_model()
        load_whisper_model()
        load_search_dependencies()
        print("--- ✅ All models initialized. ---\n")
    except Exception as e:
        print(f"❌ FATAL ERROR during model initialization: {e}")
        return

    # --- 2. Run Test Cases ---
    results = []
    for case in TEST_CASES:
        print(f"\n--- Running Test Case: {case['name']} ---")
        print(f"Description: {case['description']}")
        
        image_path = os.path.join(case['path'], "leaf_image.jpg")
        audio_path = os.path.join(case['path'], "query.wav")

        if not os.path.exists(image_path) or not os.path.exists(audio_path):
            print("❌ SKIPPING: Test assets not found for this case.")
            continue
        
        # We will capture the output of the pipeline for the report
        # Note: This requires modifying the main function slightly or redirecting stdout.
        # For simplicity here, we'll call the functions and you'll observe the console output.
        # A more advanced setup would capture stdout to a file.
        
        # For now, we just run the pipeline and manually observe the console logs.
        run_full_pipeline(image_path, audio_path)
        
        print(f"--- Finished Test Case: {case['name']} ---")

    print("\n\n" + "="*60)
    print("          Evaluation Complete")
    print("="*60)
    print("\nPlease review the console output for each test case to manually assess performance.")
    print("This output will be used to fill the evaluation table in the README.md.")


if __name__ == "__main__":
    setup_dummy_test_files()
    run_evaluation()

