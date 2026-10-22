import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent
WORDS_DIR = BASE_DIR / "words"

def load_wordlist(filename: str) -> set[str]:
    path = WORDS_DIR / filename
    if not path.exists():
        print(f"[warn] {path} niet gevonden, lege lijst gebruikt")
        return set()

    words = set()
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip().lower()
            if line and not line.startswith("#"):
                words.add(line)
    return words

SHORTENERS = load_wordlist("shorteners.txt")
SUS_WORDS = load_wordlist("sus_words.txt")

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

def analyze_url(value: str):
    parsed = urlparse(value if "://" in value else f"https://{value}")
    hostname = (parsed.hostname or "").lower()
    haystack = f"{hostname}{parsed.path}{parsed.query}".lower()

    reasons = []

    if hostname in SHORTENERS:
        reasons.append("This URL uses a URL shortening service.")

    found_words = sorted(word for word in SUS_WORDS if word in haystack)
    if found_words:
        reasons.append(
            f"This URL contains suspicious words: {', '.join(found_words)}."
        )

    if reasons:
        return {
            "status": "Suspicious",
            "message": " ".join(reasons),
        }

    return {
        "status": "ok",
        "message": "No known URL shortener detected.",
    }

@app.get("/api/health")
def health():
    uptime = datetime.now(timezone.utc) - start_time

    return {
        "message": "Backend API running",
        "uptime": int(uptime.total_seconds()),
        "status": "online",
    }

@app.post("/api/check")
def check(body: CheckRequest):
    return {
        "url": body.url,
        **analyze_url(body.url),
    }