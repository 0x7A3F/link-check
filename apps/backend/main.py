import hashlib
import os
import secrets
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
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

CHECKS = Counter("linkcheck_checks", "URLs checked", ["result"])
FLAG_REASONS = Counter("linkcheck_flag_reasons", "Reasons a URL was flagged", ["reason"])
PAGE_VIEWS = Counter("linkcheck_page_views", "Homepage views")
UNIQUE_VISITORS = Gauge("linkcheck_unique_visitors_today", "Unique visitors since 00:00 UTC")

for result in ("flagged", "clean"):
    CHECKS.labels(result)
for reason in ("shortener", "sus_words"):
    FLAG_REASONS.labels(reason)

visitor_day = date.min
visitor_salt = b""
visitor_hashes: set[str] = set()

def record_visitor(ip: str):
    global visitor_day, visitor_salt
    today = datetime.now(timezone.utc).date()
    if today != visitor_day:
        visitor_day = today
        visitor_salt = secrets.token_bytes(16)
        visitor_hashes.clear()

    visitor_hashes.add(hashlib.sha256(visitor_salt + ip.encode()).hexdigest())
    UNIQUE_VISITORS.set(len(visitor_hashes))

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

class VisitRequest(BaseModel):
    ip: str = ""

def analyze_url(value: str):
    parsed = urlparse(value if "://" in value else f"https://{value}")
    hostname = (parsed.hostname or "").lower()
    haystack = f"{hostname}{parsed.path}{parsed.query}".lower()

    reasons = []

    if hostname in SHORTENERS:
        FLAG_REASONS.labels("shortener").inc()
        reasons.append("This URL uses a URL shortening service.")

    found_words = sorted(word for word in SUS_WORDS if word in haystack)
    if found_words:
        FLAG_REASONS.labels("sus_words").inc()
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
    result = analyze_url(body.url)
    CHECKS.labels("flagged" if result["status"] == "Suspicious" else "clean").inc()

    return {
        "url": body.url,
        **result,
    }

@app.post("/api/visit", status_code=204)
def visit(body: VisitRequest):
    PAGE_VIEWS.inc()
    if body.ip:
        record_visitor(body.ip)

@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
