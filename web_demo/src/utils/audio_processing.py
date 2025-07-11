# --- src/utils/audio_processing.py ---

import whisper
from gtts import gTTS
import os
import torch
import tempfile
from pathlib import Path

# --- Configuration ---
# Use a smaller, efficient Whisper model suitable for on-device use
WHISPER_MODEL_SIZE = "base" 
# Directory to save temporary audio files
TTS_OUTPUT_DIR = os.path.join(tempfile.gettempdir(), "krishi_sahayak_audio")
os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)

# --- Model Loading (with caching) ---
whisper_model = None

def load_whisper_model():
    """
    Loads the Whisper model into memory.
    This is called once to initialize the model.
    """
    global whisper_model
    if whisper_model is None:
        print(f"Loading Whisper model ({WHISPER_MODEL_SIZE})...")
        try:
            # Check for GPU availability
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {device}")
            whisper_model = whisper.load_model(WHISPER_MODEL_SIZE, device=device)
            print("Whisper model loaded successfully.")
        except Exception as e:
            print(f"Error loading Whisper model: {e}")
            raise

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes an audio file to text using Whisper.

    Args:
        audio_file_path (str): Path to the audio file (e.g., .wav, .mp3).

    Returns:
        str: The transcribed text, or an error message.
    """
    # Ensure the whisper model is loaded
    if whisper_model is None:
        load_whisper_model()
        if whisper_model is None:
            return "Error: Whisper model could not be loaded."

    # Verify audio file path
    if not os.path.exists(audio_file_path):
        return "Error: Audio file not found."

    try:
        print(f"Transcribing audio file: {audio_file_path}")
        result = whisper_model.transcribe(audio_file_path)
        transcribed_text = result["text"]
        print(f"Transcription complete: \"{transcribed_text}\"")
        return transcribed_text
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return "Sorry, could not understand the audio."

def text_to_speech(text: str, lang: str = 'hi', slow: bool = False) -> str:
    """
    Converts text to speech using gTTS and saves it as an MP3 file.

    Args:
        text (str): The text to convert to speech.
        lang (str): The language of the text (e.g., 'en', 'hi').
        slow (bool): Whether to read the text slowly.

    Returns:
        str: The path to the generated audio file, or an error message.
    """
    if not text:
        return "Error: No text provided for text-to-speech."

    try:
        # Generate a unique filename in the temp directory
        output_file = os.path.join(TTS_OUTPUT_DIR, f"tts_output_{int(time.time())}.mp3")
        
        # Ensure the directory exists (should be created at module load)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Create the gTTS object
        tts = gTTS(text=text, lang=lang, slow=slow)

        # Save the audio file
        print(f"Generating audio file at: {output_file}")
        tts.save(output_file)
        print("Audio file generated successfully.")
        
        return output_file
    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")
        return "Sorry, could not generate audio for the response."

# --- Self-test block ---
if __name__ == '__main__':
    print("--- Running Audio Processing Self-Test ---")

    # 1. Test Text-to-Speech
    print("\n[Step 1/2] Testing Text-to-Speech...")
    test_text_hindi = "नमस्ते, मैं कृषि सहायक हूँ।"
    hindi_audio_path = text_to_speech(test_text_hindi, lang='hi')
    print(f"Hindi audio saved to: {hindi_audio_path}")

    test_text_english = "This is a test of the audio system."
    english_audio_path = text_to_speech(test_text_english, lang='en')
    print(f"English audio saved to: {english_audio_path}")

    # 2. Test Transcription (requires a sample audio file)
    print("\n[Step 2/2] Testing Transcription...")
    # For this test to work, you must place a sample audio file at this path
    sample_audio = "../data/test_assets/sample_audio.wav" 
    
    if os.path.exists(sample_audio):
        transcribed_text = transcribe_audio(sample_audio)
        print(f"\nTranscribed Text: '{transcribed_text}'")
    else:
        print(f"\nSkipping transcription test: Sample file not found at '{sample_audio}'")
        print("Please add a .wav or .mp3 file to test transcription.")
    
    print("\n--- Self-Test Complete ---")
