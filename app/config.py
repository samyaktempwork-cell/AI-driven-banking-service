from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Banking Service"

    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@banking-db:5432/banking"

    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = ConfigDict(env_file=".env")


settings = Settings()