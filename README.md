# MURFAI – AI-Powered Text-to-Speech Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-🚀-green)
![MurfAI](https://img.shields.io/badge/Murf%20AI-TTS-orange)
![AssemblyAI](https://img.shields.io/badge/AssemblyAI-STT-yellow)
![GoogleGemini](https://img.shields.io/badge/Google-Gemini-lightblue)
![License](https://img.shields.io/badge/License-MIT-purple)

---
## 📌 Overview
MURFAI is an AI-powered Text-to-Speech (TTS) application built with **FastAPI** and integrated with **Murf AI API** for generating high-quality speech from text.  
The project provides REST APIs to upload text or files and receive generated speech in multiple formats.

---
## 🚀 Features
- Convert text into natural-sounding speech
- Upload files and process them into speech
- API integration with Murf AI
- Support for multiple voice profiles
- FastAPI backend with REST endpoints
- Configurable environment variables

---

## 🛠 Technologies Used
- **Python 3.9+**
- **FastAPI**
- **httpx**
- **dotenv**
- **Pydantic**
- **Murf AI API**
- **Assembly AI API**
- **Google Generative AI API**

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
|--------|-----------------|----------------------------|
| POST   | `/upload`        | Upload text/file for TTS    |
| GET    | `/audio/{id}`    | Retrieve generated audio    |
| GET    | `/`              | Home / API status           |

---

## 📸 Screenshots
Home Page <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/363a9e76-ef25-47bf-a461-31cfd829e56b" />
Main Page <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/c695f390-cc9b-4f33-a3cd-adcc6127e9a6" />


---

## 📜 License
This project is licensed under the MIT License.
