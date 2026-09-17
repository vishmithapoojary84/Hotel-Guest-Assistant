from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat
from app.core.config import FRONTEND_URL

app = FastAPI(title="Hotel Guest Assistant API")

# Allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}
