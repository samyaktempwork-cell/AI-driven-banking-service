from fastapi import FastAPI
from app.core.logging import setup_logging
from app.config import settings

setup_logging()

app = FastAPI(title=settings.APP_NAME)

@app.get("/health/live")
def health_live():
    return {"status": "live"}

@app.get("/health/ready")
def health_ready():
    return {"status": "ready"}