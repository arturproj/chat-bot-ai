from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL del frontend Vue (Vite)
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers.chatgpt import router as chatgpt

app.include_router(chatgpt, prefix="/api")