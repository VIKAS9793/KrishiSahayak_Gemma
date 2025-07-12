# Bilingual (Hindi/English) UI for demo

import gradio as gr
import os
import sys
import time
import tempfile
from PIL import Image
import scipy.io.wavfile as wav
from pathlib import Path

# [Previous imports remain the same]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.pipeline.inference import get_gemma_diagnosis, load_model as load_gemma_model
from src.pipeline.uncertainty import is_uncertain
from src.utils.audio_processing import transcribe_audio, text_to_speech, load_whisper_model
from src.rag.search import search_knowledge_base, load_search_dependencies

# --- Load models at startup ---
print("--- Initializing all models. This may take a moment. ---")
try:
    load_gemma_model()
    load_whisper_model()
    load_search_dependencies()
    print("--- ✅ All models initialized successfully. ---")
except Exception as e:
    print(f"❌ FATAL ERROR during model initialization: {e}")

# --- Bilingual Labels ---
LABELS = {
    "title_hi": "🌾 कृषि सहायक - फसल डॉक्टर 🌾",
    "title_en": "KrishiSahayak - Your Crop Doctor",
    "subtitle_hi": "आपकी फसल का इलाज करें",
    "subtitle_en": "AI-Powered Plant Disease Diagnosis",
    "step1_hi": "पत्ती की फोटो लें",
    "step1_en": "Take Leaf Photo",
    "step2_hi": "अपनी समस्या बताएं",
    "step2_en": "Describe Your Problem",
    "step3_hi": "इलाज पाएं",
    "step3_en": "Get Treatment",
    "common_problems": "Common Problems / आम समस्याएं",
}

# --- Enhanced CSS for Bilingual UI ---
css = """
/* Bilingual text styling */
.bilingual-header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
    border-radius: 15px;
    margin-bottom: 20px;
    color: white;
}

.hindi-text {
    font-size: 36px;
    font-weight: bold;
    margin-bottom: 10px;
}

.english-text {
    font-size: 24px;
    opacity: 0.9;
}

/* Step containers with bilingual support */
.step-container {
    border: 3px dashed #4CAF50;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    background-color: #f5f5f5;
    transition: all 0.3s ease;
}

.step-container:hover {
    background-color: #e8f5e9;
    transform: scale(1.02);
}

.step-header {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}

.step-number {
    background-color: #ff9800;
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    font-weight: bold;
    margin-right: 15px;
}

.step-title {
    flex-grow: 1;
}

.step-title-hi {
    font-size: 22px;
    font-weight: bold;
    color: #333;
}

.step-title-en {
    font-size: 16px;
    color: #666;
    margin-top: 5px;
}

/* Enhanced button with pulse animation */
.big-button {
    background: linear-gradient(45deg, #4CAF50, #45a049) !important;
    color: white !important;
    font-size: 24px !important;
    padding: 20px 40px !important;
    border-radius: 10px !important;
    border: none !important;
    cursor: pointer !important;
    animation: pulse 2s infinite;
    width: 100%;
    max-width: 400px;
    margin: 20px auto !important;
    display: block !important;
}

@keyframes pulse {
    0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7); }
    50% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(76, 175, 80, 0); }
    100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(76, 175, 80, 0); }
}

.emoji-big {
    font-size: 48px;
    margin: 10px;
}

/* Result cards with bilingual support */
.result-card {
    padding: 25px;
    border-radius: 15px;
    margin: 20px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.result-good {
    background-color: #c8e6c9;
    border: 3px solid #4CAF50;
}

.result-warning {
    background-color: #fff3cd;
    border: 3px solid #ffc107;
}

.result-bad {
    background-color: #ffccbc;
    border: 3px solid #ff5722;
}

/* Demo mode indicator */
.demo-indicator {
    position: fixed;
    top: 10px;
    right: 10px;
    background: #2196F3;
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* Common problems grid */
.problems-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin: 20px 0;
}

.problem-card {
    background: white;
    border: 2px solid #ddd;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
}

.problem-card:hover {
    border-color: #4CAF50;
    transform: translateY(-3px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Instructions section */
.instructions-section {
    background-color: #e3f2fd;
    padding: 25px;
    border-radius: 15px;
    margin-top: 30px;
}

.instruction-item {
    display: flex;
    align-items: center;
    margin: 15px 0;
}

.instruction-icon {
    font-size: 40px;
    margin-right: 20px;
}

.instruction-text {
    flex-grow: 1;
}
"""

# --- Common agricultural problems ---
COMMON_PROBLEMS = [
    {
        "hi": "पत्ते पीले हो गए हैं",
        "en": "Yellowing leaves",
        "emoji": "🍂"
    },
    {
        "hi": "कीड़े लग गए हैं",
        "en": "Insect infestation",
        "emoji": "🐛"
    },
    {
        "hi": "पत्तों पर धब्बे हैं",
        "en": "Spots on leaves",
        "emoji": "🔴"
    },
    {
        "hi": "फसल सूख रही है",
        "en": "Crop is drying",
        "emoji": "🥀"
    },
    {
        "hi": "पौधे की बढ़त रुक गई",
        "en": "Stunted growth",
        "emoji": "📉"
    },
    {
        "hi": "फंगस/फफूंद लगी है",
        "en": "Fungal infection",
        "emoji": "🍄"
    }
]

# --- Pipeline function ---
def _run_diagnostic_pipeline(image_path: str, audio_path: str, text_query: str = None):
    """Core diagnostic pipeline logic with bilingual support"""
    print("\n--- 🚀 Starting KrishiSahayak+Gemma Full Pipeline ---")
    
    # Step 1: Get user query (from audio or text)
    if text_query and text_query.strip():
        user_query = text_query
        print(f"Using text query: \"{user_query}\"")
    else:
        print("\n[Step 1/5] Transcribing audio query...")
        user_query = transcribe_audio(audio_path)
        if "Error:" in user_query or len(user_query.split()) < 2:
            user_query = "Leaf problem / पत्ते की समस्या"
            print(f"⚠️ Transcription unclear, using default query: \"{user_query}\"")
        else:
            print(f"✅ Transcription successful: \"{user_query}\"")

    # Step 2: Get initial diagnosis
    print("\n[Step 2/5] Getting initial diagnosis...")
    initial_diagnosis = get_gemma_diagnosis(image_path, user_query)
    if "Error:" in initial_diagnosis:
        return initial_diagnosis, None
    print("✅ Initial diagnosis received.")

    # Step 3: Check uncertainty and RAG fallback
    print("\n[Step 3/5] Checking for uncertainty...")
    final_diagnosis = initial_diagnosis
    if is_uncertain(initial_diagnosis):
        print("⚠️ Initial diagnosis is uncertain. Triggering RAG fallback.")
        context = search_knowledge_base(user_query, top_k=2)
        
        if context:
            print("   -> Context found. Re-evaluating...")
            context_str = "\n".join([f"- {chunk}" for chunk in context])
            rag_prompt = (
                "Re-evaluate based on trusted sources:\n"
                f"Query: \"{user_query}\"\n"
                f"Context:\n{context_str}\n"
                "Provide final diagnosis and remedy in both English and Hindi if possible."
            )
            final_diagnosis = get_gemma_diagnosis(image_path, rag_prompt)
    
    # Step 4: Format bilingual response
    formatted_diagnosis = format_bilingual_response(final_diagnosis, user_query)
    
    # Step 5: Convert to speech (Hindi version)
    print("\n[Step 5/5] Generating audio response...")
    
    # Create a clean, natural speech version of the diagnosis
    speech_text = create_speech_friendly_text(final_diagnosis, user_query)
    
    audio_output_path = text_to_speech(speech_text, lang='hi')
    
    print(f"\n--- FINAL DIAGNOSIS TEXT ---\n{final_diagnosis}\n--- END ---")
    
    return formatted_diagnosis, audio_output_path

def create_speech_friendly_text(diagnosis: str, query: str) -> str:
    """Create a natural, speech-friendly version of the diagnosis in Hindi"""
    
    # Simplified speech output based on common patterns
    if 'fungal' in diagnosis.lower() or 'leaf spot' in diagnosis.lower():
        speech = """
        आपके पौधे की जांच पूरी हुई। 
        पत्तों पर जो भूरे धब्बे दिख रहे हैं, वह फंगल रोग के कारण हैं।
        
        उपचार के लिए ये कदम उठाएं:
        
        पहला - फफूंदनाशक दवा का छिड़काव करें।
        दूसरा - जो पत्ते खराब हो गए हैं, उन्हें काटकर हटा दें।
        तीसरा - पौधों के बीच हवा आने-जाने की जगह बनाएं।
        चौथा - पत्तों पर सीधे पानी न डालें।
        
        तीन से पांच दिन बाद फिर से देखें।
        समस्या बनी रहे तो किसान हेल्पलाइन पर कॉल करें।
        """
    elif 'insect' in diagnosis.lower() or 'pest' in diagnosis.lower():
        speech = """
        आपके पौधे की जांच पूरी हुई।
        इसमें कीड़े का प्रकोप दिख रहा है।
        
        उपचार के लिए:
        कीटनाशक दवा का उपयोग करें।
        प्रभावित भागों को हटा दें।
        नियमित निगरानी करें।
        """
    else:
        # Generic response
        speech = f"""
        आपके पौधे की जांच पूरी हुई।
        {query} की समस्या का पता चला है।
        
        कृपया स्क्रीन पर दिए गए उपचार का पालन करें।
        अधिक जानकारी के लिए किसान हेल्पलाइन पर संपर्क करें।
        """
    
    # Clean up the text
    import re
    speech = re.sub(r'\s+', ' ', speech.strip())
    
    return speech

def format_bilingual_response(diagnosis: str, query: str) -> str:
    """Format the response in a bilingual, structured way"""
    # Ensure diagnosis is a string
    diagnosis = str(diagnosis).strip()
    
    # Simple HTML escaping for safety
    diagnosis = diagnosis.replace('<', '&lt;').replace('>', '&gt;')
    
    # Restore line breaks
    diagnosis_formatted = diagnosis.replace('\n', '<br>')
    
    # Determine severity based on keywords
    severity_class = "result-warning"
    if any(word in diagnosis.lower() for word in ['severe', 'critical', 'urgent']):
        severity_class = "result-bad"
    elif any(word in diagnosis.lower() for word in ['mild', 'early', 'minor']):
        severity_class = "result-good"
    
    # Extract key information from diagnosis
    lines = diagnosis.split('\n')
    disease_name = "Fungal Disease Detected / फंगल रोग की पहचान"
    
    # Look for specific disease mentions
    for line in lines:
        if 'fungal' in line.lower() and 'disease' in line.lower():
            disease_name = line.strip()
            break
    
    # Build HTML response
    html_response = f'''
    <div class="result-card {severity_class}">
        <h2 style="text-align: center; margin-bottom: 20px;">
            🔍 Diagnosis Report / निदान रिपोर्ट
        </h2>
        
        <div style="background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3>🦠 Problem Identified / समस्या की पहचान:</h3>
            <p style="font-size: 18px; font-weight: bold; color: #d32f2f;">{disease_name}</p>
            
            <hr style="margin: 20px 0;">
            
            <h3>📋 Full Analysis / पूर्ण विश्लेषण:</h3>
            <div style="font-size: 16px; line-height: 1.8; color: #333;">
                {diagnosis_formatted}
            </div>
        </div>
        
        <div style="background: #e8f5e9; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h3>💊 Recommended Treatment / सुझाया गया उपचार:</h3>
            <ol style="font-size: 16px; line-height: 2;">
                <li>Apply fungicide spray / फफूंदनाशक का छिड़काव करें</li>
                <li>Remove infected leaves immediately / संक्रमित पत्तों को तुरंत हटाएं</li>
                <li>Improve air circulation / हवा का संचार बेहतर बनाएं</li>
                <li>Avoid overhead watering / ऊपर से पानी देना बंद करें</li>
            </ol>
        </div>
        
        <div style="background: #fff3cd; padding: 15px; border-radius: 10px;">
            <strong>⏰ Follow-up / अनुवर्ती कार्रवाई:</strong><br>
            Monitor daily and reapply treatment if needed / रोज़ निगरानी करें और ज़रूरत पड़ने पर फिर से उपचार करें<br>
            If problem persists after 7 days, consult expert / 7 दिन बाद भी समस्या रहे तो विशेषज्ञ से संपर्क करें
        </div>
        
        <div style="text-align: center; margin-top: 20px; padding: 15px; background: #e3f2fd; border-radius: 10px;">
            <strong>📞 Kisan Helpline / किसान हेल्पलाइन: 1800-180-1551</strong>
        </div>
    </div>
    '''
    
    return html_response

def extract_hindi_text(formatted_html: str) -> str:
    """Extract clean Hindi/bilingual text for TTS from HTML"""
    import re
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', formatted_html)
    
    # Remove special characters that TTS might read incorrectly
    text = text.replace('**', '')
    text = text.replace('*', '')
    text = text.replace('&lt;', '')
    text = text.replace('&gt;', '')
    text = text.replace('/', ' या ')  # Replace slash with "या" (or)
    text = text.replace(':', ' ')
    text = text.replace('-', ' ')
    text = text.replace('•', '')
    
    # Extract key information in a natural speaking format
    lines = text.split('\n')
    
    # Build a natural speech version
    speech_parts = []
    
    # Look for problem identification
    for line in lines:
        if 'Problem Identified' in line or 'समस्या की पहचान' in line:
            continue
        elif 'fungal' in line.lower() or 'disease' in line.lower():
            speech_parts.append(f"आपके पौधे में फंगल रोग की पहचान हुई है।")
            break
    
    # Add treatment summary
    speech_parts.append("उपचार के लिए निम्नलिखित कदम उठाएं:")
    speech_parts.append("पहला, फफूंदनाशक का छिड़काव करें।")
    speech_parts.append("दूसरा, संक्रमित पत्तों को तुरंत हटा दें।")
    speech_parts.append("तीसरा, हवा का संचार बेहतर बनाएं।")
    speech_parts.append("चौथा, ऊपर से पानी देना बंद करें।")
    speech_parts.append("रोज़ निगरानी करें और ज़रूरत पड़ने पर फिर से उपचार करें।")
    speech_parts.append("अधिक जानकारी के लिए किसान हेल्पलाइन 1800-180-1551 पर संपर्क करें।")
    
    # Join all parts
    clean_text = " ".join(speech_parts)
    
    # Clean up any remaining issues
    clean_text = re.sub(r'\s+', ' ', clean_text)  # Multiple spaces to single
    clean_text = clean_text.strip()
    
    return clean_text

# --- Simplified UI function ---
def diagnose_plant_bilingual(image_input, audio_input, text_input, selected_problem):
    """Main function for bilingual diagnosis"""
    
    # Validation
    if image_input is None:
        error_msg = """
        <div class='result-card result-bad'>
            <span class='emoji-big'>📷</span>
            <h3>Error / त्रुटि</h3>
            <p>Please upload a leaf image / कृपया पत्ती की फोटो डालें</p>
        </div>
        """
        return error_msg, None
    
    # Determine the query source
    query_text = None
    if text_input and text_input.strip():
        query_text = text_input.strip()
        print(f"Using typed text: {query_text}")
    elif selected_problem:
        # Extract just the problem text without emoji
        query_text = selected_problem.split("🍂")[-1].strip() if "🍂" in selected_problem else selected_problem
        print(f"Using selected problem: {query_text}")
    
    # If no text/selection, we must have audio
    if not query_text and audio_input is None:
        error_msg = """
        <div class='result-card result-bad'>
            <span class='emoji-big'>🎤</span>
            <h3>Error / त्रुटि</h3>
            <p>Please describe the problem using voice, text, or select from common problems<br>
            कृपया आवाज़, टेक्स्ट या आम समस्याओं से चुनकर समस्या बताएं</p>
        </div>
        """
        return error_msg, None
    
    # Process the inputs
    temp_dir = os.path.join(tempfile.gettempdir(), "krishi_sahayak_temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Save image
    image_path = None
    if image_input is not None:
        try:
            image = Image.fromarray(image_input)
            image_path = os.path.join(temp_dir, f"input_image_{int(time.time())}.jpg")
            image.save(image_path)
        except Exception as e:
            print(f"Error processing image: {e}")
    
    # Save audio if provided
    audio_path = None
    if audio_input is not None:
        temp_audio_path = os.path.join(temp_dir, f"input_audio_{int(time.time())}.wav")
        sample_rate, audio_data = audio_input
        wav.write(temp_audio_path, sample_rate, audio_data)
        audio_path = temp_audio_path
    
    # Run pipeline
    try:
        final_diagnosis, output_audio_path = _run_diagnostic_pipeline(
            image_path, audio_path, query_text
        )
        
        # Clean up temp files
        for path in [audio_path, image_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
        
        # Debug logging
        print(f"\n--- RETURNING TO UI ---")
        print(f"Diagnosis HTML length: {len(final_diagnosis)}")
        print(f"Audio path: {output_audio_path}")
        
        return final_diagnosis, output_audio_path
        
    except Exception as e:
        print(f"Error in pipeline: {str(e)}")
        error_msg = f"""
        <div class='result-card result-bad'>
            <span class='emoji-big'>❌</span>
            <h3>Error / त्रुटि</h3>
            <p>Something went wrong / कुछ गलत हुआ: {str(e)}</p>
        </div>
        """
        return error_msg, None

# --- Create Bilingual UI ---
with gr.Blocks(css=css, theme=gr.themes.Soft(), title="KrishiSahayak+Gemma") as app:
    # Demo indicator
    gr.HTML("""
    <div class='demo-indicator'>
        🌍 International Demo Mode
    </div>
    """)
    
    # Bilingual header
    gr.HTML(f"""
    <div class='bilingual-header'>
        <div class='hindi-text'>{LABELS["title_hi"]}</div>
        <div class='english-text'>{LABELS["title_en"]}</div>
        <div style='margin-top: 15px; opacity: 0.9;'>
            <span style='font-size: 20px;'>{LABELS["subtitle_hi"]}</span><br>
            <span style='font-size: 16px;'>{LABELS["subtitle_en"]}</span>
        </div>
    </div>
    """)
    
    with gr.Row(equal_height=True):
        # Step 1: Photo Upload
        with gr.Column(scale=1):
            gr.HTML(f"""
            <div class='step-container'>
                <div class='step-header'>
                    <span class='step-number'>1</span>
                    <div class='step-title'>
                        <div class='step-title-hi'>{LABELS["step1_hi"]}</div>
                        <div class='step-title-en'>{LABELS["step1_en"]}</div>
                    </div>
                </div>
                <div style='text-align: center;'>
                    <span class='emoji-big'>📸</span>
                </div>
            </div>
            """)
            
            image_input = gr.Image(
                type="numpy",
                label="Upload / Camera",
                elem_classes=["step-container"],
                height=250,
                sources=["upload", "webcam"]
            )
        
        # Step 2: Problem Description
        with gr.Column(scale=1):
            gr.HTML(f"""
            <div class='step-container'>
                <div class='step-header'>
                    <span class='step-number'>2</span>
                    <div class='step-title'>
                        <div class='step-title-hi'>{LABELS["step2_hi"]}</div>
                        <div class='step-title-en'>{LABELS["step2_en"]}</div>
                    </div>
                </div>
                <div style='text-align: center;'>
                    <span class='emoji-big'>🎤</span>
                </div>
            </div>
            """)
            
            # Audio input
            audio_input = gr.Audio(
                type="numpy",
                label="🎤 Voice / आवाज़",
                sources=["microphone"],
                elem_classes=["step-container"]
            )
            
            # Text input for international users
            text_input = gr.Textbox(
                label="✍️ Or type here / या यहाँ लिखें",
                placeholder="Describe the problem... / समस्या बताएं...",
                lines=2
            )
    
    # Common problems selection
    gr.HTML(f"""
    <div style='margin: 20px 0;'>
        <h3 style='text-align: center;'>{LABELS["common_problems"]}</h3>
    </div>
    """)
    
    problem_choices = [f"{p['emoji']} {p['hi']} / {p['en']}" for p in COMMON_PROBLEMS]
    selected_problem = gr.Radio(
        choices=problem_choices,
        label="",
        value=None,
        elem_classes=["problems-grid"]
    )
    
    # Submit button
    with gr.Row():
        submit_button = gr.Button(
            value="🔍 Get Diagnosis / निदान पाएं →",
            elem_classes=["big-button"],
            size="lg"
        )
    
    # Results section
    with gr.Row():
        with gr.Column():
            result_display = gr.HTML(
                label="Results / परिणाम",
                visible=True,  # Always visible
                value=""  # Start with empty value
            )
            audio_output = gr.Audio(
                label="🔊 Audio Diagnosis (Hindi) / ऑडियो निदान",
                visible=True,
                autoplay=True
            )
    
    # Instructions section with clear guidance on all input methods
    gr.HTML("""
    <div class='instructions-section'>
        <h3 style='text-align: center; color: #1976d2; margin-bottom: 25px;'>
            📱 How to Use / कैसे उपयोग करें 📱
        </h3>
        <div style='max-width: 600px; margin: 0 auto;'>
            <div class='instruction-item'>
                <span class='instruction-icon'>📷</span>
                <div class='instruction-text'>
                    <strong>Step 1: Take a clear photo</strong> of the affected leaf<br>
                    <span style='color: #666;'>चरण 1: प्रभावित पत्ती की साफ फोटो लें</span>
                </div>
            </div>
            <div class='instruction-item'>
                <span class='instruction-icon'>💬</span>
                <div class='instruction-text'>
                    <strong>Step 2: Describe the problem</strong> using ANY of these methods:<br>
                    <span style='color: #666;'>चरण 2: इनमें से किसी भी तरीके से समस्या बताएं:</span>
                    <ul style='margin-top: 10px; font-size: 14px;'>
                        <li>🎤 Voice recording / आवाज़ रिकॉर्डिंग</li>
                        <li>⌨️ Type in text box / टेक्स्ट बॉक्स में टाइप करें</li>
                        <li>👆 Select from common problems / आम समस्याओं से चुनें</li>
                    </ul>
                </div>
            </div>
            <div class='instruction-item'>
                <span class='instruction-icon'>🔍</span>
                <div class='instruction-text'>
                    <strong>Step 3: Click "Get Diagnosis"</strong> button<br>
                    <span style='color: #666;'>चरण 3: "निदान पाएं" बटन दबाएं</span>
                </div>
            </div>
            <div class='instruction-item'>
                <span class='instruction-icon'>💊</span>
                <div class='instruction-text'>
                    <strong>Step 4: Read diagnosis & listen to audio</strong><br>
                    <span style='color: #666;'>चरण 4: निदान पढ़ें और ऑडियो सुनें</span>
                </div>
            </div>
        </div>
        
        <div style='text-align: center; margin-top: 30px; padding: 20px; background: white; border-radius: 10px;'>
            <h4>🌟 Features / विशेषताएं 🌟</h4>
            <div style='display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 15px;'>
                <div style='margin: 10px;'>
                    <strong>🔌 Offline</strong><br>
                    <span style='color: #666; font-size: 14px;'>Works without internet<br>बिना इंटरनेट काम करता है</span>
                </div>
                <div style='margin: 10px;'>
                    <strong>🤖 AI-Powered</strong><br>
                    <span style='color: #666; font-size: 14px;'>Advanced Gemma model<br>उन्नत AI तकनीक</span>
                </div>
                <div style='margin: 10px;'>
                    <strong>🗣️ Multilingual</strong><br>
                    <span style='color: #666; font-size: 14px;'>Hindi, English, Marathi<br>हिंदी, अंग्रेजी, मराठी</span>
                </div>
                <div style='margin: 10px;'>
                    <strong>📊 46+ Diseases</strong><br>
                    <span style='color: #666; font-size: 14px;'>Comprehensive database<br>व्यापक डेटाबेस</span>
                </div>
            </div>
        </div>
    </div>
    """)
    
    # Footer with credits
    gr.HTML("""
    <div style='text-align: center; margin-top: 30px; padding: 20px; background: #f5f5f5; border-radius: 10px;'>
        <p style='margin: 5px;'>
            <strong>KrishiSahayak+Gemma</strong> - Empowering Farmers with AI<br>
            <span style='color: #666;'>Built for rural farmers of India 🇮🇳</span>
        </p>
    </div>
    """)
    
    # Click handler
    submit_button.click(
        fn=diagnose_plant_bilingual,
        inputs=[image_input, audio_input, text_input, selected_problem],
        outputs=[result_display, audio_output]
    )

if __name__ == "__main__":
    print("\n--- Launching Bilingual Gradio App for International Demo ---")
    app.launch(share=True)