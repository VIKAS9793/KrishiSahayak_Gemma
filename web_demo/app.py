# --- app/app.py ---
# This file creates a simple, user-friendly Gradio interface for our application.

import gradio as gr
import os
import sys
import time

# --- Setup System Path ---
# This ensures we can import our custom modules from the src directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# --- Import Core Logic ---
from pipeline.inference import get_gemma_diagnosis, load_model as load_gemma_model
from pipeline.uncertainty import is_uncertain
from utils.audio_processing import transcribe_audio, text_to_speech, load_whisper_model
from rag.search import search_knowledge_base, load_search_dependencies

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

# --- Main Processing Function ---
def diagnose_plant(image_input, audio_input):
    """
    This is the main function that Gradio will call.
    It takes the user's inputs and runs the entire pipeline.

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
    # Gradio provides inputs as numpy arrays, so we save them to disk
    # for our backend functions to use.
    from PIL import Image
    
    temp_dir = "temp_app_files"
    os.makedirs(temp_dir, exist_ok=True)
    
    image_path = os.path.join(temp_dir, "input_image.jpg")
    Image.fromarray(image_input).save(image_path)
    
    # Save audio file
    sample_rate, audio_data = audio_input
    audio_path = os.path.join(temp_dir, "input_audio.wav")
    import scipy.io.wavfile as wav
    wav.write(audio_path, sample_rate, audio_data)
    
    # --- Execute the full pipeline ---
    # 1. Transcribe audio
    user_query = transcribe_audio(audio_path)
    if "Error:" in user_query: return user_query, None

    # 2. Get initial diagnosis
    initial_diagnosis = get_gemma_diagnosis(image_path, user_query)
    if "Error:" in initial_diagnosis: return initial_diagnosis, None

    # 3. Check for uncertainty and perform RAG fallback if needed
    final_diagnosis = initial_diagnosis
    if is_uncertain(initial_diagnosis):
        print("⚠️ Initial diagnosis uncertain. Triggering RAG.")
        context = search_knowledge_base(user_query, top_k=2)
        if context:
            from main import construct_rag_prompt # Re-using our prompt constructor
            rag_prompt = construct_rag_prompt(user_query, context)
            final_diagnosis = get_gemma_diagnosis(image_path, rag_prompt)
        else:
            final_diagnosis += "\n\n(Note: The model was uncertain and no additional context was found in the knowledge base.)"

    # 4. Generate audio response
    # For this demo, we assume the final diagnosis is in English and generate Hindi audio.
    hindi_response_text = f"आपके पौधे का विश्लेषण: {final_diagnosis}"
    output_audio_path = text_to_speech(hindi_response_text, lang='hi')
    if "Error:" in output_audio_path: return final_diagnosis, None

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

print("\n--- Launching Gradio App ---")
app.launch(share=True) # share=True creates a public link for easy testing
