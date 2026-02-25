from app.core.logging_config import setup_logging
setup_logging()
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
import time

from app.config import settings
from app.database import engine, Base

from app.routers.auth import router as auth_router
from app.routers.transaction import router as transactions_router
from app.routers.cards import router as cards_router
from app.routers.statements import router as statements_router
from app.routers.accounts import router as accounts_router
from app.routers import health



app = FastAPI(title=settings.APP_NAME)


# -------------------------------
# Include Routers
# -------------------------------

app.include_router(auth_router)
app.include_router(transactions_router)
app.include_router(cards_router)
app.include_router(statements_router)
app.include_router(accounts_router)
app.include_router(health.router)


# -------------------------------
# Startup Logic (DB Retry)
# -------------------------------

@app.on_event("startup")
def startup():
    retries = 10
    while retries:
        try:
            Base.metadata.create_all(bind=engine)
            print("Database connected successfully")
            break
        except OperationalError:
            print("Database not ready... retrying")
            retries -= 1
            time.sleep(3)

    if retries == 0:
        raise Exception("Database connection failed after retries")


# -------------------------------
# Health Endpoints
# -------------------------------

@app.get("/health/live")
def liveness_check():
    return {"status": "alive"}


@app.get("/health/ready")
def readiness_check():
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}