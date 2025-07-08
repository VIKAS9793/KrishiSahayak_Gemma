# --- main.py ---
# The main entry point for the KrishiSahayak+Gemma application.
# This script orchestrates the full multimodal pipeline, now with RAG fallback.

import os
import sys
import time

# Add the source directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from pipeline.inference import get_gemma_diagnosis, load_model as load_gemma_model
from pipeline.uncertainty import is_uncertain
from utils.audio_processing import transcribe_audio, text_to_speech, load_whisper_model
from rag.search import search_knowledge_base, load_search_dependencies

def construct_rag_prompt(original_query: str, context_chunks: list[str]) -> str:
    """
    Constructs a detailed prompt for Gemma using the retrieved context from the generic knowledge base.

    Args:
        original_query (str): The initial user query.
        context_chunks (list[str]): A list of relevant text snippets from the knowledge base.

    Returns:
        str: A context-rich prompt with structured guidance for the model.
    """
    # Format context chunks with clear separation
    context_str = "\n\n".join([
        f"CONTEXT SOURCE {i+1}:\n{chunk.strip()}" 
        for i, chunk in enumerate(context_chunks)
    ])
    
    prompt = (
        "You are an agricultural assistant providing expert advice based on a comprehensive knowledge base. "
        "The user has provided a query about a potential plant health issue. "
        "Here is the most relevant information from our knowledge base:\n\n"
        f"{context_str}\n\n"
        "USER QUERY: "
        f"{original_query}\n\n"
        "INSTRUCTIONS:\n"
        "1. Analyze the provided context and user query carefully.\n"
        "2. Provide a clear, concise diagnosis if possible, or explain why more information is needed.\n"
        "3. If suggesting a remedy, be specific about:\n"
        "   - Any recommended treatments or actions\n"
        "   - Application methods and dosages if applicable\n"
        "   - Expected outcomes and timelines\n"
        "4. If the context doesn't fully address the query, clearly state any limitations.\n\n"
        "RESPONSE:"
    )
    return prompt

def run_full_pipeline(image_path: str, audio_path: str):
    """
    Orchestrates the full multimodal pipeline from audio/image input to audio output.
    """
    print("--- 🚀 Starting KrishiSahayak+Gemma Full Pipeline ---")
    start_time = time.time()

    # --- Step 1: Transcribe the user's voice query ---
    print("\n[Step 1/5] Transcribing audio query...")
    user_query = transcribe_audio(audio_path)
    if "Error:" in user_query:
        print(f"❌ {user_query}"); return
    print(f"✅ Transcription successful: \"{user_query}\"")

    # --- Step 2: Get initial diagnosis from Gemma ---
    print("\n[Step 2/5] Getting initial diagnosis...")
    initial_diagnosis = get_gemma_diagnosis(image_path, user_query)
    if "Error:" in initial_diagnosis:
        print(f"❌ {initial_diagnosis}"); return
    print("✅ Initial diagnosis received.")

    # --- Step 3: Check for uncertainty ---
    print("\n[Step 3/5] Checking for uncertainty...")
    final_diagnosis = initial_diagnosis
    if is_uncertain(initial_diagnosis):
        print("⚠️ Initial diagnosis is uncertain. Triggering RAG fallback.")
        
        # --- Step 3a: Search knowledge base ---
        print("\n   -> Searching knowledge base for context...")
        context = search_knowledge_base(user_query, top_k=3)
        
        if context:
            print("   -> Context found. Re-evaluating with new prompt...")
            # --- Step 3b: Construct new prompt and re-query ---
            rag_prompt = construct_rag_prompt(user_query, context)
            final_diagnosis = get_gemma_diagnosis(image_path, rag_prompt)
            print("   -> ✅ Re-evaluation complete.")
        else:
            print("   -> ⚠️ No relevant context found in knowledge base. Using initial diagnosis.")
    else:
        print("✅ Initial diagnosis is confident. Skipping RAG fallback.")

    print("\n[Step 4/5] Final Diagnosis Received.")
    print("\n--- Final Model Diagnosis (Text) ---")
    print(final_diagnosis)
    print("------------------------------------")

    # --- Step 5: Convert the diagnosis to speech ---
    print("\n[Step 5/5] Generating audio response...")
    response_text_hindi = f"आपके पौधे की समस्या का विश्लेषण: {final_diagnosis}"
    audio_output_path = text_to_speech(response_text_hindi, lang='hi')
    
    if "Error:" in audio_output_path:
        print(f"❌ {audio_output_path}")
    else:
        print(f"✅ Audio response generated at: {audio_output_path}")

    end_time = time.time()
    print(f"\n--- ✅ Pipeline finished in {end_time - start_time:.2f} seconds ---")


if __name__ == "__main__":
    print("--- Initializing all models. This may take a moment. ---")
    load_gemma_model()
    load_whisper_model()
    load_search_dependencies()
    print("--- All models initialized. Ready to start. ---\n")

    TEST_IMAGE_PATH = "data/test_assets/sample_leaf.jpg"
    TEST_AUDIO_PATH = "data/test_assets/sample_audio.wav"

    if not os.path.exists(TEST_IMAGE_PATH) or not os.path.exists(TEST_AUDIO_PATH):
        print("Error: Test assets not found. Please check paths.")
    else:
        run_full_pipeline(image_path=TEST_IMAGE_PATH, audio_path=TEST_AUDIO_PATH)

# --- src/pipeline/inference.py ---

import torch
from transformers import AutoProcessor, Gemma3nForConditionalGeneration, BitsAndBytesConfig
from PIL import Image
import os

MODEL_ID = "google/gemma-3n-e2b-it"
model = None
processor = None

def load_model():
    global model, processor
    if model is None:
        print("Loading Gemma 3n model...")
        quantization_config = BitsAndBytesConfig(load_in_4bit=True)
        try:
            cache_dir = "./model_cache"
            model = Gemma3nForConditionalGeneration.from_pretrained(
                MODEL_ID,
                quantization_config=quantization_config,
                torch_dtype=torch.bfloat16,
                cache_dir=cache_dir
            )
            processor = AutoProcessor.from_pretrained(MODEL_ID, cache_dir=cache_dir)
            print("✅ Gemma model loaded.")
        except Exception as e:
            print(f"❌ Error loading Gemma model: {e}"); raise

def get_gemma_diagnosis(image_path: str, user_query: str) -> str:
    if model is None or processor is None:
        load_model()
    if not os.path.exists(image_path):
        return "Error: Image file not found."
    try:
        image = Image.open(image_path).convert("RGB")
        prompt = f"<image>\n<start_of_turn>user\n{user_query}<end_of_turn>\n<start_of_turn>model\n"
        inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)
        generation_output = model.generate(**inputs, max_new_tokens=250, do_sample=False)
        response_text = processor.decode(generation_output[0], skip_special_tokens=True)
        return response_text.split("model\n")[-1].strip()
    except Exception as e:
        print(f"❌ Error during inference: {e}"); return "Error during inference."

# --- src/pipeline/uncertainty.py ---

import re

UNCERTAINTY_KEYWORDS = ["not sure", "unsure", "cannot determine", "unclear", "difficult to say", "not confident", "could be", "might be", "appears to be", "seems like", "no diagnosis", "insufficient information"]
MIN_RESPONSE_LENGTH_WORDS = 8

def is_uncertain(response: str) -> bool:
    if not response: return True
    lower_response = response.lower()
    for keyword in UNCERTAINTY_KEYWORDS:
        if keyword in lower_response:
            print(f"⚠️ Uncertainty detected (keyword: '{keyword}')"); return True
    word_count = len(re.findall(r'\w+', lower_response))
    if word_count < MIN_RESPONSE_LENGTH_WORDS:
        print(f"⚠️ Uncertainty detected (short response: {word_count} words)"); return True
    print("✅ Response deemed confident."); return False

# --- src/rag/build_index.py ---

import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

EMBEDDING_MODEL_ID_RAG = 'all-MiniLM-L6-v2'
RAW_DATA_PATH = "../data/raw/sample_knowledge_base.csv"
PROCESSED_DATA_DIR_RAG = "../data/processed"
INDEX_FILE_PATH = os.path.join(PROCESSED_DATA_DIR_RAG, "knowledge_base.faiss")
TEXT_DATA_PATH = os.path.join(PROCESSED_DATA_DIR_RAG, "knowledge_base_text.pkl")

def create_text_chunks(df: pd.DataFrame) -> list[str]:
    chunks = []
    for _, row in df.iterrows():
        chunks.append(f"Disease: {row['disease_name']}. Symptoms: {row['symptoms']}. Remedy: {row['remedy']}. Source: {row['source']}.")
    return chunks

def build_and_save_index():
    print("--- Starting Knowledge Base Indexing ---")
    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ ERROR: Raw data file not found at '{RAW_DATA_PATH}'."); return
    df = pd.read_csv(RAW_DATA_PATH).fillna("Not available")
    text_chunks = create_text_chunks(df)
    model = SentenceTransformer(EMBEDDING_MODEL_ID_RAG)
    embeddings = model.encode(text_chunks, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings, dtype=np.float32))
    os.makedirs(PROCESSED_DATA_DIR_RAG, exist_ok=True)
    faiss.write_index(index, INDEX_FILE_PATH)
    with open(TEXT_DATA_PATH, 'wb') as f: pickle.dump(text_chunks, f)
    print("\n--- ✅ Knowledge Base Indexing Complete ---")

if __name__ == 'build_index': build_and_save_index()

# --- src/rag/search.py ---

import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL_ID_SEARCH = 'all-MiniLM-L6-v2'
PROCESSED_DATA_DIR_SEARCH = "../data/processed"
INDEX_FILE_PATH_SEARCH = os.path.join(PROCESSED_DATA_DIR_SEARCH, "knowledge_base.faiss")
TEXT_DATA_PATH_SEARCH = os.path.join(PROCESSED_DATA_DIR_SEARCH, "knowledge_base_text.pkl")

embedding_model_search = None
index_search = None
text_data_search = None

def load_search_dependencies():
    global embedding_model_search, index_search, text_data_search
    if embedding_model_search is None:
        embedding_model_search = SentenceTransformer(EMBEDDING_MODEL_ID_SEARCH)
    if index_search is None:
        index_search = faiss.read_index(INDEX_FILE_PATH_SEARCH)
    if text_data_search is None:
        with open(TEXT_DATA_PATH_SEARCH, 'rb') as f: text_data_search = pickle.load(f)

def search_knowledge_base(query: str, top_k: int = 3) -> list[str]:
    load_search_dependencies()
    query_embedding = embedding_model_search.encode([query])
    _, indices = index_search.search(np.array(query_embedding, dtype=np.float32), top_k)
    return [text_data_search[i] for i in indices[0]]

# --- src/utils/audio_processing.py ---

import whisper
from gtts import gTTS

WHISPER_MODEL_SIZE = "base"
TTS_OUTPUT_DIR = "../data/processed/audio_outputs"
whisper_model = None

def load_whisper_model():
    global whisper_model
    if whisper_model is None:
        print(f"Loading Whisper model ({WHISPER_MODEL_SIZE})...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        whisper_model = whisper.load_model(WHISPER_MODEL_SIZE, device=device)
        print("✅ Whisper model loaded.")

def transcribe_audio(audio_file_path: str) -> str:
    if whisper_model is None: load_whisper_model()
    if not os.path.exists(audio_file_path): return "Error: Audio file not found."
    try:
        result = whisper_model.transcribe(audio_file_path)
        return result["text"]
    except Exception as e:
        print(f"❌ Error during transcription: {e}"); return "Error during transcription."

def text_to_speech(text: str, lang: str = 'hi', slow: bool = False) -> str:
    if not text: return "Error: No text provided."
    try:
        os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)
        tts = gTTS(text=text, lang=lang, slow=slow)
        output_path = os.path.join(TTS_OUTPUT_DIR, f"{hash(text)}.mp3")
        tts.save(output_path)
        return output_path
    except Exception as e:
        print(f"❌ Error during TTS: {e}"); return "Error during TTS."
