🎙️ Voice AI Assistant
A modern, interactive voice assistant web application built with Streamlit that provides real-time voice interaction with beautiful visual feedback.

✨ Features
🎯 Core Functionality
Real-time Voice Transcription: Convert speech to text using Groq API

AI-Powered Responses: Get intelligent responses from RAG system

Text-to-Speech: Audio playback of AI responses

Conversation Memory: Maintains chat history and context

🎨 Visualization
Interactive Voice Visualization: Animated circles respond to voice input

Multiple Color Themes: Choose from 6 beautiful color schemes

Real-time Animation: Visual feedback during recording and processing

Customizable Effects: Adjust animation speed and pulse effects

💬 User Interface
Clean Chat Interface: Differentiated user/assistant messages

Session Statistics: Track questions asked and responses given

Responsive Design: Works on desktop and mobile devices

Sidebar Controls: Easy access to settings and stats

🚀 Quick Start
Prerequisites
Python 3.8 or higher

Groq API key

Streamlit

Installation
Clone the repository

bash
git clone https://github.com/yourusername/voice-ai-assistant.git
cd voice-ai-assistant
Create virtual environment (optional but recommended)

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Set up environment variables

bash
export GROQ_API_KEY="your_groq_api_key_here"  # On Windows: set GROQ_API_KEY=your_groq_api_key_here
Running the Application
bash
streamlit run main.py
The application will open in your default web browser at http://localhost:8501

📁 Project Structure
text
voice-ai-assistant/
├── main.py                    # Main Streamlit application
├── groq_transcriber.py        # Audio transcription module
├── rag_system.py             # RAG system for AI responses
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .env.example             # Environment variables template
🔧 Configuration
Environment Variables
Create a .env file in the project root:

env
GROQ_API_KEY=your_groq_api_key_here
Color Themes
Choose from 6 built-in color themes:

Blue (Default)

Purple

Red

Green

Orange

Neon

Animation Settings
Animation Speed: Slow, Normal, Fast

Pulse Effect: Enable/disable pulse animation

Circle Size: Small, Medium, Large

🎮 How to Use
Start the application using streamlit run main.py

Configure settings in the sidebar:

Choose color theme

Adjust animation preferences

View session statistics

Record your voice:

Click the "Start Voice" button

Speak clearly into your microphone

Watch the visualization respond to your voice

View responses:

See transcribed text

Listen to AI-generated audio response

Chat history is automatically saved

🛠️ Technical Details
Dependencies
streamlit: Web application framework

gTTS: Google Text-to-Speech for audio generation

groq: For voice transcription API

python-dotenv: Environment variable management

Key Components
Voice Transcription: Uses Groq API for accurate speech-to-text

RAG System: Provides context-aware responses

Visualization Engine: Real-time animated feedback

Session Management: Maintains conversation state

📱 Browser Support
Chrome (recommended)

Firefox

Safari

Edge

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Streamlit for the amazing web app framework

Groq for voice transcription API

Google TTS for text-to-speech functionality

📞 Support
For support, please open an issue in the GitHub repository or contact the maintainers.

🚧 Roadmap
Add support for multiple languages

Implement voice recognition for different accents

Add export chat history feature

Implement user authentication

Add more visualization options

Create mobile app version

⭐ Star this repo if you find it useful! ⭐

Made with ❤️ by Raman