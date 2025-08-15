from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from services.stt_service import transcribe_file
from services.tts_service import tts_single, tts_chunks
from services.llm_service import generate_reply
from schemas.voice_schemas import TTSRequest
from utils.helpers import (
    save_upload_file,
    split_for_murf,
    ensure_dirs,
    FALLBACK_AUDIO,
    STATIC_WELCOME,
    STATIC_INDEX,
)

# Ensure required directories exist on import
ensure_dirs()

router = APIRouter()

# In-memory chat histories (same behavior as your original code)
chat_histories: dict[str, list[dict[str, str]]] = {}

@router.get("/")
async def welcome():
    return FileResponse(STATIC_WELCOME)

@router.get("/mika")
async def serve_ui():
    return FileResponse(STATIC_INDEX)

@router.post("/tts")
async def tts_endpoint(request: TTSRequest):
    try:
        audio_url = await tts_single(request.text)
        return {"audio_url": audio_url}
    except Exception as e:
        print(f"[ERROR] /tts failed: {e}")
        return JSONResponse(
            status_code=502,
            content={"audio_url": FALLBACK_AUDIO, "error": "TTS service unavailable"},
        )

@router.post("/agent/chat/{session_id}")
async def agent_chat(session_id: str, file: UploadFile = File(...)):
    try:
        # 1) Save upload
        fpath = await save_upload_file(file)

        # 2) STT
        try:
            user_text = await transcribe_file(fpath)
        except Exception as e:
            print(f"[ERROR] STT failed: {e}")
            return JSONResponse(
                status_code=502,
                content={"audio_urls": [FALLBACK_AUDIO], "error": "STT service unavailable"},
            )

        if not user_text:
            return JSONResponse({"error": "Empty transcription"}, status_code=400)

        # 3) Build history + prompt
        history = chat_histories.get(session_id, [])
        history.append({"role": "user", "content": user_text})
        full_prompt = "\n".join([f"{m['role']}: {m['content']}" for m in history])

        # 4) LLM with fallbacks
        try:
            assistant_text, model_used = await generate_reply(full_prompt)

            # Remove unwanted "assistant:" prefix if present
            assistant_text = assistant_text.lstrip()
            if assistant_text.lower().startswith("assistant:"):
                assistant_text = assistant_text[len("assistant:"):].lstrip()

            print(f"[INFO] LLM model used: {model_used}")
        except Exception as e:
            print(f"[ERROR] LLM failed: {e}")
            return JSONResponse(
                status_code=502,
                content={"audio_urls": [FALLBACK_AUDIO], "error": "LLM service unavailable"},
            )

        history.append({"role": "assistant", "content": assistant_text})
        chat_histories[session_id] = history

        # 5) TTS (chunked)
        chunks = split_for_murf(assistant_text)
        audio_urls = await tts_chunks(chunks)

        return {
            "transcription": user_text,
            "llm_response": assistant_text,
            "audio_urls": audio_urls,
            "history": history,
        }
    except Exception as e:
        print(f"[ERROR] Chat endpoint failed: {e}")
        return JSONResponse(
            status_code=500,
            content={"audio_urls": [FALLBACK_AUDIO], "error": "Internal server error"},
        )
