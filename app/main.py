from fastapi import FastAPI, Depends

from app.core.logging import setup_logging
from app.config import settings
from app.database import engine, Base
import app.models  # ensures models are registered
from app.routers import auth
from app.core.security import get_current_user
from app.models.user import User
from app.routers import auth, account, transaction


setup_logging()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth.router)

app.include_router(account.router)

app.include_router(transaction.router)

@app.get("/health/live")
def health_live():
    return {"status": "live"}


@app.get("/health/ready")
def health_ready():
    return {"status": "ready"}


# Temporary protected test route
@app.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
    }