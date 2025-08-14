from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os, time
import shutil
import httpx
from dotenv import load_dotenv
import assemblyai as aai
import google.generativeai as genai

load_dotenv()
MURF_API_KEY = os.getenv("MURF_API_KEY")
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

aai.settings.api_key = ASSEMBLYAI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)
transcriber = aai.Transcriber()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "uploads"
TRANSCRIBE_DIR = os.path.join("static", "transcribe")
FALLBACK_AUDIO = "/static/error.wav"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(TRANSCRIBE_DIR, exist_ok=True)

chat_histories = {}

class TTSRequest(BaseModel):
    text: str

class LLMQuery(BaseModel):
    text: str

@app.get("/")
def welcome():
    return FileResponse("static/welcome.html")  # your welcome page HTML

# Serve your main UI at "/mika"
@app.get("/mika")
def serve_ui():
    return FileResponse("static/index.html")

def split_for_murf(text, max_chars=3000):
    chunks = []
    current = ""
    for word in text.split():
        if len(current) + len(word) + 1 > max_chars:
            chunks.append(current.strip())
            current = word
        else:
            current += " " + word
    if current.strip():
        chunks.append(current.strip())
    return chunks

async def call_gemini_model(prompt: str, model_name: str):
    """Call Gemini model and return text, or raise Exception."""
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text.rstrip("\n")

@app.post("/tts")
async def tts(request: TTSRequest):
    try:
        url = "https://api.murf.ai/v1/speech/generate"
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "api-key": MURF_API_KEY,
        }
        payload = {"text": request.text, "voice_id": "en-IN-priya", "style": "Conversational"}
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
        audio_url = data.get("audio_url") or data.get("audioFile")
        if not audio_url:
            raise HTTPException(status_code=502, detail="No audio URL from TTS service")
        return {"audio_url": audio_url}
    except Exception as e:
        print(f"[ERROR] TTS failed: {e}")
        return JSONResponse(
            status_code=502,
            content={"audio_url": FALLBACK_AUDIO, "error": "TTS service unavailable"},
        )

@app.post("/agent/chat/{session_id}")
async def agent_chat(session_id: str, file: UploadFile = File(...)):
    try:
        ext = file.filename.split(".")[-1] or "webm"
        fname = f"chat_{int(time.time()*1000)}.{ext}"
        fpath = os.path.join(UPLOAD_DIR, fname)
        with open(fpath, "wb") as buf:
            shutil.copyfileobj(file.file, buf)

        # Step 1: Speech to Text
        try:
            transcript = transcriber.transcribe(fpath)
            user_text = (transcript.text or "").strip()
        except Exception as e:
            print(f"[ERROR] STT failed: {e}")
            return JSONResponse(
                status_code=502,
                content={"audio_urls": [FALLBACK_AUDIO], "error": "STT service unavailable"},
            )

        if not user_text:
            return JSONResponse({"error": "Empty transcription"}, status_code=400)

        history = chat_histories.get(session_id, [])
        history.append({"role": "user", "content": user_text})
        full_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in history])

        # Step 2: LLM with updated fallbacks
        assistant_text = None
        try:
            assistant_text = await call_gemini_model(full_prompt, "gemini-1.5-flash")
            print("[INFO] Primary model (gemini-1.5-flash) used")
        except Exception as e:
            print(f"[WARN] Primary model failed: {e}")
            try:
                assistant_text = await call_gemini_model(full_prompt, "gemini-2.5-flash")
                print("[INFO] Fallback model (gemini-2.5-flash) used")
            except Exception as e2:
                print(f"[WARN] First fallback failed: {e2}")
                try:
                    assistant_text = await call_gemini_model(full_prompt, "gemini-2.5-pro")
                    print("[INFO] Second fallback model (gemini-2.5-pro) used")
                except Exception as e3:
                    print(f"[ERROR] All models failed: {e3}")
                    return JSONResponse(
                        status_code=502,
                        content={"audio_urls": [FALLBACK_AUDIO], "error": "LLM service unavailable"},
                    )

        history.append({"role": "assistant", "content": assistant_text})
        chat_histories[session_id] = history

        # Step 3: Text to Speech
        murf_urls = []
        for chunk in split_for_murf(assistant_text):
            try:
                murf_url = "https://api.murf.ai/v1/speech/generate"
                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/json",
                    "api-key": MURF_API_KEY,
                }
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        murf_url, headers=headers, json={"text": chunk, "voice_id": "en-IN-priya", "style": "Conversational"}
                    )
                    resp.raise_for_status()
                    data = resp.json()
                audio_url = data.get("audio_url") or data.get("audioFile")
                murf_urls.append(audio_url or FALLBACK_AUDIO)
            except Exception as e:
                print(f"[ERROR] TTS chunk failed: {e}")
                murf_urls.append(FALLBACK_AUDIO)

        return {
            "transcription": user_text,
            "llm_response": assistant_text,
            "audio_urls": murf_urls,
            "history": history,
        }
    except Exception as e:
        print(f"[ERROR] Chat endpoint failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"audio_urls": [FALLBACK_AUDIO], "error": "Internal server error"},
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4554, reload=True)
