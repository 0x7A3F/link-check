import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from datetime import datetime, timezone
from urllib.parse import urlparse

app = FastAPI(
    title="Link Checking API",
    description="Check how likely a URL is to be a scam. **Work in progress.**",
    version="0.1.0",
)

start_time = datetime.now(timezone.utc)

origins = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
class CheckRequest(BaseModel):
    url: str

SHORTENERS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "is.gd",
    "cutt.ly"
}

def analyze_url(value):
    parsed = urlparse(value if "://" in value else f"https://{value}")
    hostname = (parsed.hostname or "").lower()

    if hostname in SHORTENERS:
        return {
            "status": "Suspicious",
            "message": "This URL uses a URL shortening service."
        }

    return {
        "status": "ok",
        "message": "No known URL shortener detected."
    }

@app.get("/api/health")
def health():
    uptime = datetime.now(timezone.utc) - start_time

    return {
        "message": "Backend API running",
        "uptime": int(uptime.total_seconds()),
        "status": "online"
    }


@app.post("/api/check")
def check(body: CheckRequest):
    return {
        "url": body.url,
        **analyze_url(body.url),
    }