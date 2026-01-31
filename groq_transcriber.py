import requests
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def transcribe_audio_with_groq(audio_bytes, api_key=None, language="en"):
    """
    Transcribe audio using Groq's Whisper API
    
    Args:
        audio_bytes: Audio data as bytes
        api_key: Groq API key (optional, will use GROQ_API_KEY env var)
        language: Language code (default: "en" for English)
    
    Returns:
        tuple: (transcribed_text, error_message)
        If successful: (text, None)
        If failed: (None, error_message)
    
    Example:
        # Read audio file
        with open("recording.wav", "rb") as f:
            audio_data = f.read()
        
        text, error = transcribe_audio_with_groq(audio_data)
        if text:
            print(f"Transcription: {text}")
        else:
            print(f"Error: {error}")
    """
    # Get API key
    if api_key is None:
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return None, "API key not provided. Set GROQ_API_KEY environment variable or pass api_key parameter."
    
    # API endpoint
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    
    # Headers
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    
    # Prepare the request
    files = {
        'file': ('audio.wav', audio_bytes, 'audio/wav')
    }
    data = {
        'model': 'whisper-large-v3',
        'language': language,
        'response_format': 'json'
    }
    
    try:
        # Make the request
        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data,
            timeout=30  # 30 second timeout
        )
        
        # Check response
        if response.status_code == 200:
            result = response.json()
            text = result.get('text', '').strip()
            if text:
                return text, None
            else:
                return None, "No speech detected in audio"
        else:
            # Handle API errors
            error_msg = f"API Error {response.status_code}"
            try:
                error_detail = response.json().get('error', {}).get('message', response.text)
                error_msg += f": {error_detail}"
            except:
                error_msg += f": {response.text}"
            return None, error_msg
            
    except requests.exceptions.Timeout:
        return None, "Request timeout - server took too long to respond"
    except requests.exceptions.ConnectionError:
        return None, "Connection error - check your internet connection"
    except requests.exceptions.RequestException as e:
        return None, f"Request error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def get_groq_llm_response(prompt, api_key=None, model="mixtral-8x7b-32768"):
    """
    Get response from Groq's LLM
    
    Args:
        prompt: User input text
        api_key: Groq API key (optional)
        model: Model to use
    
    Returns:
        tuple: (response_text, error_message)
    """
    # Get API key
    if api_key is None:
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return None, "API key not provided"
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Be concise and accurate."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'], None
        else:
            return None, f"API Error {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"Error: {str(e)}"


# Simple usage example
if __name__ == "__main__":
    # Test with a file
    test_file = "test_audio.wav"  # Replace with your audio file
    
    if os.path.exists(test_file):
        print("Testing Groq transcription...")
        
        # Read audio file
        with open(test_file, "rb") as f:
            audio_data = f.read()
        
        # Transcribe
        text, error = transcribe_audio_with_groq(audio_data)
        
        if text:
            print(f"✅ Transcription: {text}")
            
            
            # Get LLM response
            print("\nGetting AI response...")
            response, error = get_groq_llm_response(text)
            
            if response:
                print(f"🤖 Response: {response}")
            else:
                print(f"❌ LLM Error: {error}")
        else:
            print(f"❌ Transcription Error: {error}")
    else:
        print(f"Test file '{test_file}' not found.")
        print("Create a test WAV file or use the function in your code.")