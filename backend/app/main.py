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

# --- ROUTERS ---
app.include_router(auth.router)
app.include_router(chat.router)

# Mount the frontend directory
# We assume "chat-frontend" is at the same level as "backend"
# So relative to "backend/app/main.py", it is "../../chat-frontend"
# But we are running from "backend", so it is "../chat-frontend"
START_DIR = os.getcwd() # This should be /backend
FRONTEND_DIR = os.path.join(START_DIR, "..", "chat-frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def root():
    # Serve index.html
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
