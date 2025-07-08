# --- scripts/generate_knowledge_base_gemma.py ---
# This script uses Gemma to generate the content for our knowledge base.

import os
import sys
import pandas as pd
import time

# --- Setup System Path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pipeline.inference import generate_text_from_prompt, load_model

# --- Configuration ---
# Use absolute path to ensure the file is found regardless of working directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISEASE_LIST_PATH = os.path.join(BASE_DIR, "data", "raw", "disease_list.txt")
OUTPUT_CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "knowledge_base.csv")

def create_generation_prompt(plant_name: str, disease_name: str) -> str:
    """Creates a precise prompt to instruct Gemma to act as an expert."""
    return (
        f"<start_of_turn>user\n"
        f"You are an expert agricultural scientist. Provide a concise description for the disease '{disease_name}' affecting '{plant_name}' plants. "
        f"Your response must be in two parts. First, a 'Symptoms:' section detailing the primary visual signs on the plant. "
        f"Second, a 'Remedy:' section listing common and effective control measures. Provide only these two sections.\n"
        f"<end_of_turn>\n<start_of_turn>model\n"
    )

def parse_generated_text(text: str) -> dict:
    """Parses the generated text to extract symptoms and remedy."""
    symptoms = "Not found."
    remedy = "Not found."
    
    try:
        # Find the 'Symptoms:' part and extract text until 'Remedy:'
        symptoms_match = pd.Series(text).str.extract(r'Symptoms:(.*?)(?=Remedy:|$)').iloc[0,0]
        if pd.notna(symptoms_match):
            symptoms = symptoms_match.strip()

        # Find the 'Remedy:' part and extract the rest of the text
        remedy_match = pd.Series(text).str.extract(r'Remedy:(.*)').iloc[0,0]
        if pd.notna(remedy_match):
            remedy = remedy_match.strip()
            
    except Exception as e:
        print(f"   -> Parsing error: {e}")
        
    return {"symptoms": symptoms, "remedy": remedy}


def main():
    """Main function to generate the knowledge base using Gemma."""
    print("--- 🤖 Starting Generative Knowledge Base Creation ---")
    
    # Load the Gemma model once
    load_model()

    if not os.path.exists(DISEASE_LIST_PATH):
        print(f"❌ ERROR: Disease list not found at '{DISEASE_LIST_PATH}'"); return

    with open(DISEASE_LIST_PATH, 'r') as f:
        disease_names = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    knowledge_data = []
    total_diseases = len(disease_names)

    for i, disease in enumerate(disease_names):
        print(f"\n--- Processing {i+1}/{total_diseases}: {disease} ---")
        
        parts = [p.strip() for p in disease.split('-')]
        plant, disease_name_part = (parts[0], parts[1]) if len(parts) == 2 else (disease, "")
        standardized_name = f"{plant}___{disease_name_part.replace(' ', '_')}"

        prompt = create_generation_prompt(plant, disease_name_part)
        generated_text = generate_text_from_prompt(prompt)
        
        if "Error" in generated_text:
            print(f"   -> ⚠️ Generation failed for {disease}.")
            extracted_info = {"symptoms": "Generation failed.", "remedy": "Generation failed."}
        else:
            print(f"   -> ✅ Text generated. Parsing...")
            extracted_info = parse_generated_text(generated_text)

        knowledge_data.append({
            "disease_name": standardized_name,
            "symptoms": extracted_info["symptoms"],
            "remedy": extracted_info["remedy"],
            "source": "Gemma 3n (Generative)"
        })
        
        time.sleep(1) # Small delay

    df = pd.DataFrame(knowledge_data)
    df.to_csv(OUTPUT_CSV_PATH, index=False)
    
    print("\n" + "="*50)
    print(f"✅ Generative knowledge base creation complete.")
    print(f"File saved to: {OUTPUT_CSV_PATH}")
    print("⚠️ IMPORTANT: Please manually review the generated CSV for factual accuracy.")
    print("="*50)

if __name__ == "__main__":
    main()
