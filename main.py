# In your Streamlit app
import streamlit as st
from groq_transcriber import transcribe_audio_with_groq
import os
import pyttsx3
from rag_system import rag_system

speach = pyttsx3.init()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Record audio
audio_bytes = st.audio_input("Record your voice")

def speachs(response):
    
    print(f"\nAssistant: {response}")
    speach.say(response)
    speach.runAndWait()
    speach.stop()

if audio_bytes:
    # Display audio
    st.audio(audio_bytes)
    
    # Transcribe
    with st.spinner("Transcribing..."):
        text, error = transcribe_audio_with_groq(audio_bytes, api_key)
        
        if text:
            st.success(f"Transcription: {text}")
            # Use text with your RAG system
            response = rag_system.get_response(text)
            if response:
                speachs(response)
        else:
            st.error(f"Error: {error}")