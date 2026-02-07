from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, chat

print("MAIN LOADED")

app = FastAPI()

# --- CORS MUST COME BEFORE ROUTERS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

# --- ROUTERS ---
app.include_router(auth.router)
app.include_router(chat.router)

# Mount the frontend directory
# file is backend/app/main.py
# parent is backend/app
# parent.parent is backend
# parent.parent.parent is project root
# project root / chat-frontend is what we want

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "chat-frontend"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
def root():
    # Serve index.html
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"status": "ok", "message": "Frontend not found"}
