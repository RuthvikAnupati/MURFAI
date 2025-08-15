import os
import time
import shutil
from fastapi import UploadFile

# Paths & constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder where helpers.py is
PROJECT_ROOT = os.path.dirname(BASE_DIR)  # one level up: D:\PROJECTS\MURFAI
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "uploads")
STATIC_DIR = os.path.join(PROJECT_ROOT, "static")
TRANSCRIBE_DIR = os.path.join(STATIC_DIR, "transcribe")

FALLBACK_AUDIO = "/static/error.wav"
STATIC_WELCOME = os.path.join(STATIC_DIR, "welcome.html")
STATIC_INDEX = os.path.join(STATIC_DIR, "index.html")

# Ensure directory existence
def ensure_dirs() -> None:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(TRANSCRIBE_DIR, exist_ok=True)

async def save_upload_file(file: UploadFile) -> str:
    ext = (file.filename or "").split(".")[-1] or "webm"
    fname = f"chat_{int(time.time() * 1000)}.{ext}"
    fpath = os.path.join(UPLOAD_DIR, fname)
    with open(fpath, "wb") as buf:
        shutil.copyfileobj(file.file, buf)
    return fpath

# Keep your original chunking approach (tuned for Murf)
def split_for_murf(text: str, max_chars: int = 3000) -> list[str]:
    chunks: list[str] = []
    current = ""
    for word in text.split():
        if len(current) + len(word) + 1 > max_chars:
            if current.strip():
                chunks.append(current.strip())
            current = word
        else:
            current += " " + word
    if current.strip():
        chunks.append(current.strip())
    return chunks
