import os
import httpx
from dotenv import load_dotenv
from utils.helpers import FALLBACK_AUDIO

load_dotenv()

MURF_API_KEY = os.getenv("MURF_API_KEY")
if not MURF_API_KEY:
    raise RuntimeError("MURF_API_KEY is not set")

MURF_URL = "https://api.murf.ai/v1/speech/generate"
MURF_HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
    "api-key": MURF_API_KEY,
}

VOICE_PAYLOAD_BASE = {"voice_id": "en-IN-priya", "style": "Conversational"}

async def tts_single(text: str) -> str:
    payload = {**VOICE_PAYLOAD_BASE, "text": text}
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(MURF_URL, headers=MURF_HEADERS, json=payload)
        resp.raise_for_status()
        data = resp.json()
    audio_url = data.get("audio_url") or data.get("audioFile")
    if not audio_url:
        raise RuntimeError("No audio URL from TTS service")
    return audio_url

async def tts_chunks(chunks: list[str]) -> list[str]:
    urls: list[str] = []
    async with httpx.AsyncClient(timeout=60) as client:
        for chunk in chunks:
            try:
                payload = {**VOICE_PAYLOAD_BASE, "text": chunk}
                resp = await client.post(MURF_URL, headers=MURF_HEADERS, json=payload)
                resp.raise_for_status()
                data = resp.json()
                audio_url = data.get("audio_url") or data.get("audioFile") or FALLBACK_AUDIO
                urls.append(audio_url)
            except Exception as e:
                print(f"[ERROR] TTS chunk failed: {e}")
                urls.append(FALLBACK_AUDIO)
    return urls