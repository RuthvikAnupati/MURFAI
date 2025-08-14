# MURFAI – AI-Powered Text-to-Speech Platform

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
- **Google Generative AI API** (if applicable)

---

## 📂 Project Structure
```
project-root/
│── main.py                  # FastAPI entry point
│── requirements.txt         # Python dependencies
│── .env                     # Environment variables
│── static/                  # Static files
│── templates/               # HTML templates (if any)
│── README.md                # Project documentation
```
---

## 🏗 Architecture
1. **Frontend / API Client** sends text or file to the backend API.
2. **FastAPI server** processes the request.
3. **Murf AI API** generates the speech file.
4. The generated audio is stored locally or returned as a response.

---

## ⚙ Environment Variables
Create a `.env` file in the project root with:
```
MURF_API_KEY=your_murf_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
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
uvicorn main:app --reload --port 8000
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
*(Add screenshots in `/static/screenshots/` and reference here)*

---

## 📜 License
This project is licensed under the MIT License.
