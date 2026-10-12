from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
def health():
    return {
        "message": "Backend API running",
        "status": "online"
    }