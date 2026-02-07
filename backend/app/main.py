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

# --- ROUTERS ---
app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {"status": "ok"}
