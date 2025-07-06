# --- app.py (Merged & Refactored) ---
# This file contains the complete, user-friendly Gradio interface and the
# full backend pipeline logic for the KrishiSahayak+Gemma web demo.

import gradio as gr
import os
import sys
import time
from PIL import Image
import scipy.io.wavfile as wav

# --- Setup System Path ---
# This ensures we can import our custom modules from the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# --- Import Core Logic Modules ---
from src.pipeline.inference import get_gemma_diagnosis, load_model as load_gemma_model
from src.pipeline.uncertainty import is_uncertain
from src.utils.audio_processing import transcribe_audio, text_to_speech, load_whisper_model
from src.rag.search import search_knowledge_base, load_search_dependencies

# --- Load all models at startup ---
# This is a time-consuming process that should only happen once.
print("--- Initializing all models. This may take a moment. ---")
try:
    load_gemma_model()
    load_whisper_model()
    load_search_dependencies()
    print("--- ✅ All models initialized successfully. ---")
except Exception as e:
    print(f"❌ FATAL ERROR during model initialization: {e}")
    # In a real app, you might exit or display a persistent error message.

# --- Core Pipeline Logic ---
def _run_diagnostic_pipeline(image_path: str, audio_path: str):
    """
    This internal function contains the full, step-by-step diagnostic logic.
    It is called by the Gradio interface function.

    Args:
        image_path (str): The path to the input image file.
        audio_path (str): The path to the input audio file.

    Returns:
        tuple: A tuple containing the final diagnosis text and the path to the output audio file.
    """
    print("\n--- 🚀 Starting KrishiSahayak+Gemma Full Pipeline ---")
    
    # --- Step 1: Transcribe the user's voice query ---
    print("\n[Step 1/5] Transcribing audio query...")
    user_query = transcribe_audio(audio_path)
    if "Error:" in user_query:
        return user_query, None
    print(f"✅ Transcription successful: \"{user_query}\"")

    # --- Step 2: Get initial diagnosis from Gemma ---
    print("\n[Step 2/5] Getting initial diagnosis...")
    initial_diagnosis = get_gemma_diagnosis(image_path, user_query)
    if "Error:" in initial_diagnosis:
        return initial_diagnosis, None
    print("✅ Initial diagnosis received.")

    # --- Step 3: Check for uncertainty and perform RAG fallback ---
    print("\n[Step 3/5] Checking for uncertainty...")
    final_diagnosis = initial_diagnosis
    if is_uncertain(initial_diagnosis):
        print("⚠️ Initial diagnosis is uncertain. Triggering RAG fallback.")
        
        # --- Step 3a: Search knowledge base ---
        print("\n   -> Searching knowledge base for context...")
        context = search_knowledge_base(user_query, top_k=2)
        
        if context:
            print("   -> Context found. Re-evaluating with new prompt...")
            # --- Step 3b: Construct new prompt and re-query ---
            context_str = "\n".join([f"- {chunk}" for chunk in context])
            rag_prompt = (
                "The user provided an image and a query. My initial analysis was uncertain. "
                "Please re-evaluate the user's query based on the following trusted expert sources and provide a final, confident diagnosis and remedy.\n\n"
                f"Original User Query: \"{user_query}\"\n\n"
                "Trusted Context:\n"
                f"{context_str}\n\n"
                "Based on the image and this new context, what is the final diagnosis and what is the recommended remedy?"
            )
            final_diagnosis = get_gemma_diagnosis(image_path, rag_prompt)
            print("   -> ✅ Re-evaluation complete.")
        else:
            print("   -> ⚠️ No relevant context found in knowledge base. Using initial diagnosis.")
            final_diagnosis += "\n\n(Note: The model was uncertain and no additional context was found in the knowledge base.)"
    else:
        print("✅ Initial diagnosis is confident. Skipping RAG fallback.")

    print("\n[Step 4/5] Final Diagnosis Received.")
    print("\n--- Final Model Diagnosis (Text) ---")
    print(final_diagnosis)
    print("------------------------------------")

    # --- Step 5: Convert the diagnosis to speech ---
    print("\n[Step 5/5] Generating audio response...")
    # For this demo, we assume the final diagnosis is in English and generate Hindi audio.
    hindi_response_text = f"आपके पौधे का विश्लेषण: {final_diagnosis}"
    audio_output_path = text_to_speech(hindi_response_text, lang='hi')
    if "Error:" in audio_output_path:
        return final_diagnosis, None

    return final_diagnosis, audio_output_path

# --- Gradio Interface Function ---
def diagnose_plant(image_input, audio_input):
    """
    This is the main function that Gradio will call. It acts as a wrapper that
    handles the web inputs/outputs and calls the core pipeline logic.

    Args:
        image_input (numpy.ndarray): The image provided by the user.
        audio_input (tuple): A tuple containing (sample_rate, numpy_array) for the audio.

    Returns:
        tuple: A tuple containing the final diagnosis text and the path to the output audio file.
    """
    if image_input is None:
        return "Error: Please upload an image of the plant leaf.", None
    if audio_input is None:
        return "Error: Please record your question using the microphone.", None

    start_time = time.time()
    print("\n--- New Diagnosis Request Received ---")

    # --- Save temporary files for processing ---
    temp_dir = "temp_app_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    image_path = os.path.join(temp_dir, "input_image.jpg")
    Image.fromarray(image_input).save(image_path)
    
    sample_rate, audio_data = audio_input
    audio_path = os.path.join(temp_dir, "input_audio.wav")
    wav.write(audio_path, sample_rate, audio_data)
    
    # --- Execute the core pipeline logic ---
    final_diagnosis, output_audio_path = _run_diagnostic_pipeline(image_path, audio_path)

    print(f"--- Pipeline finished in {time.time() - start_time:.2f} seconds ---")
    
    return final_diagnosis, output_audio_path

# --- Create and Launch the Gradio Interface ---
with gr.Blocks(theme=gr.themes.Soft(), title="KrishiSahayak+Gemma") as app:
    gr.Markdown(
        """
        # 🚜 KrishiSahayak+Gemma
        ### An Offline, Explainable Farm Assistant
        Upload a photo of the plant leaf and ask your question using the microphone.
        """
    )
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="numpy", label="1. Upload Leaf Image")
            audio_input = gr.Audio(type="numpy", label="2. Record Your Question (in English or Marathi)", sources=["microphone"])
            submit_button = gr.Button("Diagnose Plant", variant="primary")
        with gr.Column():
            gr.Markdown("###  Diagnosis Results")
            text_output = gr.Textbox(label="Diagnosis and Remedy", lines=10)
            audio_output = gr.Audio(label="Listen to Diagnosis (in Hindi)")

    submit_button.click(
        fn=diagnose_plant,
        inputs=[image_input, audio_input],
        outputs=[text_output, audio_output]
    )

if __name__ == "__main__":
    print("\n--- Launching Gradio App ---")
    app.launch(share=True) # share=True creates a public link for easy testing
