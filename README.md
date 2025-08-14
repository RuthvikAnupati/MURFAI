# 🎙 AI Voice Assistant – FastAPI + Murf AI + AssemblyAI + Google Gemini

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-🚀-green)
![MurfAI](https://img.shields.io/badge/Murf%20AI-TTS-orange)
![AssemblyAI](https://img.shields.io/badge/AssemblyAI-STT-yellow)
![GoogleGemini](https://img.shields.io/badge/Google-Gemini-lightblue)
![License](https://img.shields.io/badge/License-MIT-purple)

---

## 📂 Project Structure
```
project-root/
│── main.py                  # FastAPI entry point
│── requirements.txt         # Python dependencies
│── .env                     # Environment variables
│── static/                  # Static assets (audio, video, icons, CSS, JS)
│   ├── favicon.ico
│   ├── error.wav
│   ├── index.html
│   ├── welcome.html
│   ├── v1.mp4
│   ├── v2.mp4
│   └── transcribe/          # Additional static resources
│
│── uploads/                 # Temporary audio uploads
│── templates/               # Jinja2 HTML templates (if any)
│── venv/                    # Virtual environment
│── README.md                # Documentation
```

---

## 🏗 System Architecture
1. **Frontend / API Client** sends text or file to the backend API.
2. **FastAPI server** processes the request.
3. **Murf AI API** generates the speech file.
4. The generated audio is stored locally or returned as a response.

```
┌──────────────────┐      ┌──────────────────┐     ┌──────────────────┐
│  🎤 Frontend UI  │────▶│ 🚀 FastAPI API  │────▶│  🧠 AI Services │
│                  │      │                  │     │                  │
│ • Audio Record   │      │ • Pipeline Mgmt  │     │ • AssemblyAI STT │
│ • Visualization  │      │ • Session Memory │     │ • Google Gemini  │
│ • Playback       │      │ • Error Handling │     │ • Murf AI TTS    │
└──────────────────┘      └──────────────────┘     └──────────────────┘
```

---

## 🔄 Pipeline Flow
1. **Audio Capture** → Browser records user speech via MediaRecorder API.
2. **Speech Recognition (STT)** → AssemblyAI transcribes audio to text.
3. **AI Processing (LLM)** → Google Gemini (or other LLM) generates a response with personality.
4. **Voice Synthesis (TTS)** → Murf AI converts response text to natural-sounding speech.
5. **Playback** → Browser plays generated voice with real-time waveform visualizations.

---

## ⚙ Environment Variables
Create a `.env` file in the project root with:
```
MURF_API_KEY=your_murf_api_key
ASSEMBLYAI_API_KEY=your_assemblyai_key
GOOGLE_API_KEY=your_google_api_key
```

---

## 🚀 Installation & Run
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-voice-assistant.git
cd ai-voice-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate   # For Windows

# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
uvicorn main:app --reload --port 8000
```

---

## 📜 License
This project is licensed under the MIT License.
