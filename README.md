# MIKA – AI-Powered Voice Agent!

## 📌 Overview
MIKA is an AI-powered application built with **FastAPI** and integrated with **Murf AI API** for generating high-quality speech from text.  
The project provides REST APIs to upload text or files and receive generated speech in multiple formats.

---

## ✨ Key Features
- 🎙 **Real-time Voice Conversations** – Talk naturally with MIKA, no typing required.
- 🎭 **Unique Personality** – Configurable conversational style for engaging AI interactions.
- 📱 **Modern UI/UX** – Glassmorphic design with smooth animations and audio visualizations.
- 🔄 **Session Persistence** – Maintains context for multi-turn conversations.
- ⚡ **Low Latency Pipeline** – Optimized for near real-time responses.
- 🛡 **Robust Error Handling** – Graceful degradation on STT/LLM/TTS failures.
- 🎵 **Audio Visualizations** – Real-time waveform feedback during recording and playback.

---

## 🛠 Technologies Used
- **Python 3.9+**
- **FastAPI** – Backend API
- **httpx** – Asynchronous HTTP client
- **dotenv** – Environment configuration
- **Pydantic** – Request/response validation
- **AssemblyAI API** – Speech-to-text
- **Google Generative AI API** – Language model processing (optional)
- **Murf AI API** – Text-to-speech synthesis
- **HTML5, CSS3, Vanilla JS** – Frontend

---

## 📂 Project Structure
```plaintext
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
---

## 🏗 System Architecture
1. **Frontend / API Client** sends text or file to the backend API.
2. **FastAPI server** processes the request.
3. **Murf AI API** generates the speech file.
4. The generated audio is stored locally or returned as a response.
┌──────────────────┐      ┌──────────────────┐     ┌──────────────────┐
│  🎤 Frontend UI  │────▶│ 🚀 FastAPI API  │────▶│  🧠 AI Services │
│                  │      │                  │     │                  │
│ • Audio Record   │      │ • Pipeline Mgmt  │     │ • AssemblyAI STT │
│ • Visualization  │      │ • Session Memory │     │ • Google Gemini  │
│ • Playback       │      │ • Error Handling │     │ • Murf AI TTS    │
└──────────────────┘      └──────────────────┘     └──────────────────┘


---
🔄 Pipeline Flow
1. Audio Capture → Browser records user speech via MediaRecorder API.
2. Speech Recognition (STT) → AssemblyAI transcribes audio to text.
3. AI Processing (LLM) → Google Gemini (or other LLM) generates a response with personality.
4. Voice Synthesis (TTS) → Murf AI converts response text to natural-sounding speech.
5. Playback → Browser plays generated voice with real-time waveform visualizations.
---

## ⚙ Environment Variables
Create a `.env` file in the project root with:
```
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
GOOGLE_API_KEY=your_google_api_key
MURF_API_KEY=your_murf_api_key

```
*(Only include GOOGLE_API_KEY if using Google Generative AI)*

---

## 📦 Installation & Running
1. **Clone the repository**
```bash
git clone https://github.com/RuthvikAnupati/MURFAI.git
cd MURFAI
```

2. **Create a virtual environment & activate**
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate    # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the API server**
```bash
uvicorn main:app --reload --port 4554
```
*(Change port number as needed)*

---

## 🔗 API Endpoints
| Method | Endpoint         | Description                |
|--------|------------------|----------------------------|
| POST   | `/upload`        | Upload text/file for TTS   |
| GET    | `/audio/{id}`    | Retrieve generated audio   |
| GET    | `/`              | Home / API status          |

---

## 📸 Screenshots
<img width="1920" height="873" alt="12 1" src="https://github.com/user-attachments/assets/1331d800-cd43-464c-a9b5-e1f0245a7ddd" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ca5e648a-f66f-49f0-88f4-fddb5c522135" />

---

## 📜 License
This project is licensed under the MIT License.
