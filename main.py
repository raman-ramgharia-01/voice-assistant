import streamlit as st
from groq_transcriber import transcribe_audio_with_groq
import os
from gtts import gTTS
import io
from rag_system import rag_system

# Page Config
st.set_page_config(page_title="Voice Assistant", page_icon="🎙️")

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# --- Updated Speech Function ---
def play_speech(text_response):
    """Generates audio from text and plays it in the Streamlit browser."""
    try:
        tts = gTTS(text=text_response, lang='en')
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        # Use autoplay so the user hears it immediately
        st.audio(audio_fp, format='audio/mp3', autoplay=True)
    except Exception as e:
        st.error(f"TTS Error: {e}")

# UI Layout
st.title("🎙️ AI Voice Assistant")

# Record audio
audio_bytes = st.audio_input("Record your voice")

if audio_bytes:
    # Transcribe
    with st.spinner("Thinking..."):
        text, error = transcribe_audio_with_groq(audio_bytes, api_key)
        
        if text:
            st.chat_message("user").write(text)
            
            # Use text with your RAG system
            response = rag_system.get_response(text)
            
            if response:
                with st.chat_message("assistant"):
                    st.write(response)
                    # Play the response audio
                    play_speech(response)
        else:
            st.error(f"Transcription failed: {error}")
            
