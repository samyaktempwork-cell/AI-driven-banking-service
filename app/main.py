from fastapi import FastAPI
from app.core.logging import setup_logging
from app.config import settings
from app.database import engine, Base
import app.models

setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

@app.get("/health/live")
def health_live():
    return {"status": "live"}

@app.get("/health/ready")
def health_ready():
    return {"status": "ready"}