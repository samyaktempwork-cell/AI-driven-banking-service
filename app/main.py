from fastapi import FastAPI
from app.config import settings
from app.database import engine, Base
from app.routers.auth import router as auth_router
from app.routers.transaction import router as transactions_router
import time
from sqlalchemy.exc import OperationalError


app = FastAPI(title=settings.APP_NAME)

app.include_router(auth_router)
app.include_router(transactions_router)


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