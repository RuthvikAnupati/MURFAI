import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set")

genai.configure(api_key=GEMINI_API_KEY)

PRIMARY_MODEL = "gemini-1.5-flash"
FALLBACK_1 = "gemini-2.5-flash"
FALLBACK_2 = "gemini-2.5-pro"

async def _call_model(prompt: str, model_name: str) -> str:
    model = genai.GenerativeModel(model_name)
    resp = model.generate_content(prompt)
    return (resp.text or "").rstrip("\n")

async def generate_reply(full_prompt: str) -> tuple[str, str]:
    try:
        text = await _call_model(full_prompt, PRIMARY_MODEL)
        return text, PRIMARY_MODEL
    except Exception as e:
        print(f"[WARN] Primary model failed: {e}")
        try:
            text = await _call_model(full_prompt, FALLBACK_1)
            return text, FALLBACK_1
        except Exception as e2:
            print(f"[WARN] First fallback failed: {e2}")
            text = await _call_model(full_prompt, FALLBACK_2)
            return text, FALLBACK_2