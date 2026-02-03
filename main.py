import streamlit as st
from groq_transcriber import transcribe_audio_with_groq
import os
from gtts import gTTS
import io
from rag_system import rag_system
import json
import random
from datetime import datetime

# Page Config
st.set_page_config(
    page_title="Voice Assistant Pro",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get API key
api_key = os.getenv("GROQ_API_KEY")

# Initialize session states
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'session_feedback' not in st.session_state:
    st.session_state.session_feedback = {
        'questions_asked': 0,
        'responses_given': 0,
        'start_time': datetime.now(),
        'last_interaction': None
    }

if 'visualization_params' not in st.session_state:
    st.session_state.visualization_params = {
        'color_theme': 'blue',
        'circle_size': 'medium',
        'animation_speed': 'normal',
        'pulse_effect': True
    }

# Color themes
COLOR_THEMES = {
    'blue': {'primary': '#00dbde', 'secondary': '#5b86e5', 'accent': '#36d1dc'},
    'purple': {'primary': '#fc00ff', 'secondary': '#a18cd1', 'accent': '#fbc2eb'},
    'red': {'primary': '#ff416c', 'secondary': '#ff4b2b', 'accent': '#ff9a9e'},
    'green': {'primary': '#00b09b', 'secondary': '#96c93d', 'accent': '#a8e6cf'},
    'orange': {'primary': '#ff9966', 'secondary': '#ff5e62', 'accent': '#ffcc00'}
}


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


# Custom CSS for animations
def inject_custom_css():
    st.html("""
    <style>
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes ripple {
        0% { transform: scale(0.8); opacity: 1; }
        100% { transform: scale(3); opacity: 0; }
    }
    
    .voice-circle {
        border-radius: 50%;
        position: absolute;
        mix-blend-mode: screen;
        transition: all 0.2s ease;
    }
    
    .pulse-circle {
        position: absolute;
        border-radius: 50%;
        animation: ripple 2s linear infinite;
        pointer-events: none;
    }
    
    .visualization-container {
        height: 300px;
        width: 100%;
        position: relative;
        background: rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 20px;
        
    }
    
    .chat-message {
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
        animation: fadeIn 0.3s ease;
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(0, 219, 222, 0.2), rgba(91, 134, 229, 0.2));
        border-left: 4px solid #00dbde;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, rgba(252, 0, 255, 0.2), rgba(161, 140, 209, 0.2));
        border-left: 4px solid #fc00ff;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .feedback-badge {
        padding: 5px 10px;
        border-radius: 10px;
        font-size: 0.8em;
        margin: 2px;
        display: inline-block;
    }
    
    .recording-indicator {
        animation: pulse 1.5s infinite;
        color: #ff416c;
    }
    
    /* Remove audio player styling */
    .stAudio {
        display: none !important;
    }
    
    .fast-response {
        transition: all 0.1s ease;
    }
    </style>
    """)

# Initialize custom CSS
inject_custom_css()

# --- REMOVED Speech Function - No audio playback needed ---

# Visualization function
def create_visualization(volume_level=50, is_recording=False, is_processing=False):
    """Creates animated circles visualization based on voice input."""
    colors = COLOR_THEMES[st.session_state.visualization_params['color_theme']]
    
    # Calculate circle sizes based on settings
    size_map = {'small': 40, 'medium': 60, 'large': 80}
    base_size = size_map[st.session_state.visualization_params['circle_size']]
    
    # Adjust animation based on state
    if is_processing:
        pulse_speed = '0.8s'
        volume_level = 80
    elif is_recording:
        pulse_speed = '1s'
        volume_level = 60
    else:
        pulse_speed = '2s'
        volume_level = 30
    
    # Create HTML for visualization
    visualization_html = f"""
    <div class="visualization-container" id="viz-container">
        <div style="
            position: absolute;
            top: 40%;
            left: 40%;
            transform: translate(-50%, -50%);
            width: {base_size * (1 + volume_level/100)}px;
            height: {base_size * (1 + volume_level/100)}px;
            background: radial-gradient(circle, {colors['primary']} 0%, transparent 70%);
            opacity: 0.6;
            animation: pulse {pulse_speed} infinite;
            transition: all 0.1s ease;
            border-radius: 50%;
            box-shadow: 0 0 30px {colors['primary']};
        "></div>
        
        <div style="
            position: absolute;
            top: 44%;
            left: 45%;
            transform: translate(-50%, -50%);
            width: {base_size * 0.7 * (1 + volume_level/120)}px;
            height: {base_size * 0.7 * (1 + volume_level/120)}px;
            background: radial-gradient(circle, {colors['secondary']} 0%, transparent 70%);
            opacity: 0.4;
            animation: pulse {'1.2s' if is_recording else '2.5s'} infinite;
            animation-delay: 0.3s;
            display: none;border-radius: 50%;
            box-shadow: 0 0 20px {colors['secondary']};
        "></div>
        
        <div style="
            display: none;
            position: absolute;
            top: 49%;
            left: 49%;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            width: {base_size * 0.4 * (1 + volume_level/150)}px;
            height: {base_size * 0.4 * (1 + volume_level/150)}px;
            background: radial-gradient(circle, {colors['accent']} 0%, transparent 70%);
            opacity: 0.8;
            animation: float 3s ease-in-out infinite;
            box-shadow: 0 0 15px {colors['accent']};
        "></div>
    """
    
    # Add floating particles
    for i in range(8):
        x = random.randint(20, 80)
        y = random.randint(20, 80)
        size = random.randint(5, 15)
        delay = random.random() * 2
        
        visualization_html += f"""
        <div style="
            position: absolute;
            top: {y}%;
            left: {x}%;
            width: {size}px;
            height: {size}px;
            background: {colors['accent']};
            border-radius: 50%;
            opacity: 0.3;
            animation: float 4s ease-in-out infinite;
            animation-delay: {delay}s;
        "></div>
        """
    
    # Add pulse effect if enabled and recording/processing
    if st.session_state.visualization_params['pulse_effect'] and (is_recording or is_processing):
        visualization_html += f"""
        <div class="pulse-circle" style="
            top: 50%;
            left: 50%;
            width: 50px;
            height: 50px;
            background: {colors['primary']};
            animation: ripple 1.5s linear infinite;
        "></div>
        """
    
    visualization_html += "</div>"
    
    return visualization_html

# Sidebar for settings and feedback
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Color Theme Selector
    st.subheader("Visualization Theme")
    theme = st.selectbox(
        "Choose color theme",
        options=list(COLOR_THEMES.keys()),
        index=list(COLOR_THEMES.keys()).index(st.session_state.visualization_params['color_theme'])
    )
    st.session_state.visualization_params['color_theme'] = theme
    
    # Circle Size
    size = st.select_slider(
        "Circle Size",
        options=['small', 'medium', 'large'],
        value=st.session_state.visualization_params['circle_size']
    )
    st.session_state.visualization_params['circle_size'] = size
    
    # Animation Speed
    speed = st.select_slider(
        "Animation Speed",
        options=['slow', 'normal', 'fast'],
        value=st.session_state.visualization_params['animation_speed']
    )
    st.session_state.visualization_params['animation_speed'] = speed
    
    # Pulse Effect Toggle
    pulse = st.toggle(
        "Enable Pulse Effect",
        value=st.session_state.visualization_params['pulse_effect']
    )
    st.session_state.visualization_params['pulse_effect'] = pulse
    
    st.divider()
    
    # Session Feedback
    st.subheader("📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Questions", st.session_state.session_feedback['questions_asked'])
    with col2:
        st.metric("Responses", st.session_state.session_feedback['responses_given'])
    
    if st.session_state.session_feedback['last_interaction']:
        st.caption(f"Last interaction: {st.session_state.session_feedback['last_interaction'].strftime('%H:%M:%S')}")
    
    # Chat History Summary
    if st.session_state.chat_history:
        st.divider()
        st.subheader("💭 Recent Chats")
        recent_chats = st.session_state.chat_history[-3:]
        
        for i, chat in enumerate(recent_chats):
            if chat['type'] == 'user':
                question_text = chat.get('question', '')[:50]
                if len(chat.get('question', '')) > 50:
                    question_text += "..."
                st.caption(f"**Q{i+1}:** {question_text}")
            elif chat['type'] == 'assistant':
                answer_text = chat.get('answer', '')[:50]
                if len(chat.get('answer', '')) > 50:
                    answer_text += "..."
                st.caption(f"**A{i+1}:** {answer_text}")
    
    # Clear Chat Button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main UI Layout
st.title("🎙️ AI Voice Assistant")
st.caption("Speak naturally and watch the visualization respond to your voice!")

# Create two columns for visualization and chat

# Visualization Display
viz_placeholder = st.empty()

# Initialize with default visualization
viz_html = create_visualization(volume_level=30, is_recording=False)
viz_placeholder.html(viz_html)


# Record audio section
# st.subheader("🎤 Voice Input")
audio_bytes = st.audio_input("Click to record your question", key="audio_input")

# Process audio if recorded
if audio_bytes:
    # Update visualization to show recording state - FAST
    recording_html = create_visualization(volume_level=60, is_recording=True)
    viz_placeholder.html(recording_html)
    
    # Transcribe - FAST
    with st.spinner("🎤 Transcribing..."):
        text, error = transcribe_audio_with_groq(audio_bytes, api_key)
        
        if text:
            # Update session feedback
            st.session_state.session_feedback['questions_asked'] += 1
            st.session_state.session_feedback['last_interaction'] = datetime.now()
            
            # Store question in chat history
            st.session_state.chat_history.append({
                'question': text,
                'timestamp': datetime.now(),
                'type': 'user'
            })
            
            # Display user message immediately
            user_message_container = st.empty()
            user_message_container.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong> {text}<br>
                <small><em>{datetime.now().strftime('%H:%M:%S')}</em></small>
            </div>
            """, unsafe_allow_html=True)
            
            # Update visualization for processing
            processing_html = create_visualization(volume_level=80, is_processing=True)
            viz_placeholder.html(processing_html)
            
            # Get context from previous chats (last 3 exchanges)
            context = ""
            if len(st.session_state.chat_history) > 1:
                recent_chats = st.session_state.chat_history[-3:-1]  # Exclude current
                for chat in recent_chats:
                    if chat['type'] == 'user':
                        context += f"Previous question: {chat['question']}\n"
                    elif chat['type'] == 'assistant':
                        context += f"Previous answer: {chat.get('answer', '')}\n"
            
            # Combine context with current question
            enhanced_query = f"{context}\nCurrent question: {text}"
            
            # Get response from RAG system - FAST
            with st.spinner("🤔 Thinking..."):
                # Remove any delays and get response immediately
                response = rag_system.get_response(enhanced_query)
                # response = "This is a fast sample response from the AI assistant."
                play_speech(response)
            
            if response:
                # Update session feedback
                st.session_state.session_feedback['responses_given'] += 1
                
                # Store assistant response in chat history
                st.session_state.chat_history.append({
                    'answer': response,
                    'timestamp': datetime.now(),
                    'type': 'assistant'
                })
                
                # Display assistant response immediately - NO AUDIO
                assistant_message_container = st.empty()
                assistant_message_container.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Assistant:</strong> {response}<br>
                    <small><em>{datetime.now().strftime('%H:%M:%S')}</em></small>
                </div>
                """, unsafe_allow_html=True)
                
                # Update visualization with success effect
                success_html = create_visualization(volume_level=70, is_processing=True)
                viz_placeholder.html(success_html)
                
                # Fast return to normal visualization
                normal_html = create_visualization(volume_level=30, is_recording=False)
                viz_placeholder.html(normal_html)
                
        else:
            st.error(f"❌ Transcription failed: {error}")
            
            # Error visualization
            error_html = """
            <div class="visualization-container" style="background: linear-gradient(135deg, rgba(255, 65, 108, 0.1), rgba(255, 75, 43, 0.1));">
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #ff416c; font-size: 2em;">
                    ❌
                </div>
            </div>
            """
            viz_placeholder.html(error_html)

# Display chat history in main area
if st.session_state.chat_history:
    st.divider()
    st.subheader("💬 Chat History")
    
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            if chat['type'] == 'user':
                st.html(f"""
                <div class="chat-message user-message">
                    <strong>👤 You:</strong> {chat['question']}<br>
                    <small><em>{chat['timestamp'].strftime('%H:%M:%S')}</em></small>
                </div>
                """)
            elif chat['type'] == 'assistant':
                st.html(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 Assistant:</strong> {chat.get('answer', '')}<br>
                    <small><em>{chat['timestamp'].strftime('%H:%M:%S')}</em></small>
                </div>
                """)

# Fast JavaScript for real-time updates
st.html("""
<script>
// Fast visualization updates
function updateVisualizationFast(volume) {
    const container = document.getElementById('viz-container');
    if (container) {
        const circles = container.getElementsByTagName('div');
        if (circles.length > 0) {
            circles[0].style.width = (60 * (1 + volume/100)) + 'px';
            circles[0].style.height = (60 * (1 + volume/100)) + 'px';
        }
    }
}

// Fast animations for recording state
if (window.location.hash === '#recording') {
    let vol = 30;
    const fastInterval = setInterval(() => {
        vol = 30 + Math.random() * 40;
        updateVisualizationFast(vol);
    }, 50); // Faster updates
}
</script>
""")

# Add footer with session info
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"Session started: {st.session_state.session_feedback['start_time'].strftime('%H:%M:%S')}")
with col2:
    duration = datetime.now() - st.session_state.session_feedback['start_time']
    minutes = int(duration.total_seconds() / 60)
    st.caption(f"Session duration: {minutes} minutes")
with col3:
    if st.session_state.chat_history:
        last_chat = st.session_state.chat_history[-1]
        if last_chat['type'] == 'user':
            last_text = last_chat.get('question', 'Question')[:20]
        else:
            last_text = last_chat.get('answer', 'Response')[:20]
        
        if len(last_text) > 20:
            last_text += "..."
        
        st.caption(f"Last: {last_text}")