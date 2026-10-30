import hashlib
import ipaddress
import os
import secrets
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, generate_latest
from pydantic import BaseModel, ConfigDict, Field

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
SUS_TLDS = load_wordlist("sus_tlds.txt")

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
for reason in ("shortener", "sus_words", "sus_tld", "ip_address", "credentials"):
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
    model_config = ConfigDict(str_strip_whitespace=True)

    url: str = Field(min_length=1, max_length=2048)

class VisitRequest(BaseModel):
    ip: str = ""

def is_shortener(hostname: str) -> bool:
    return any(
        hostname == domain or hostname.endswith(f".{domain}")
        for domain in SHORTENERS
    )

def is_ip_address(hostname: str) -> bool:
    try:
        ipaddress.ip_address(hostname)
        return True
    except ValueError:
        return False

def analyze_url(value: str):
    parsed = urlparse(value if "://" in value else f"https://{value}")
    hostname = (parsed.hostname or "").lower().rstrip(".")
    haystack = f"{hostname}{parsed.path}{parsed.query}".lower()

    reasons = []

    if is_shortener(hostname):
        FLAG_REASONS.labels("shortener").inc()
        reasons.append("This URL uses a URL shortening service.")

    tld = hostname.rsplit(".", 1)[-1] if "." in hostname else ""
    if tld in SUS_TLDS:
        FLAG_REASONS.labels("sus_tld").inc()
        reasons.append(f"This URL uses the .{tld} domain extension, which is often used for scams.")

    if is_ip_address(hostname):
        FLAG_REASONS.labels("ip_address").inc()
        reasons.append("This URL points to an IP address instead of a domain name.")

    if "@" in parsed.netloc:
        FLAG_REASONS.labels("credentials").inc()
        reasons.append(
            "This URL contains an '@' before the domain, which can hide the real destination."
        )

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
        "message": "No suspicious patterns detected.",
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
