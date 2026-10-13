from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, timezone

app = FastAPI()

start_time = datetime.now(timezone.utc)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    uptime = datetime.now(timezone.utc) - start_time

    return {
        "message": "Backend API running",
        "uptime": int(uptime.total_seconds()),
        "status": "online"
    }