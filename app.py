from dotenv import load_dotenv
load_dotenv()  # must come before importing services/routers

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from routers.voice_routes import router as voice_router
import uvicorn
import traceback
app = FastAPI(title="Voice Agent API",debug=True)

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        tb = traceback.format_exc()
        print(f"[ERROR] Unhandled exception: {e}\n{tb}")
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": tb
            }
        )

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(voice_router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=4554, reload=True)
