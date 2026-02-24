import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "AI Banking Service"
    DEBUG: bool = os.getenv("DEBUG", "False") == "True"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./banking.db")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "supersecretkey")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()