import os
import assemblyai as aai
from dotenv import load_dotenv

load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    raise RuntimeError("ASSEMBLYAI_API_KEY is not set")

aai.settings.api_key = ASSEMBLYAI_API_KEY

# Use the SDK's Transcriber in a simple async wrapper
async def transcribe_file(file_path: str) -> str:
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(file_path)
    # The SDK is synchronous; we keep API parity with your original logic
    return (transcript.text or "").strip()