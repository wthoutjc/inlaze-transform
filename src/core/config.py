import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", None)
    LOAD_URL: str = os.getenv("LOAD_URL", "http://localhost:5002")
    API_V1_STR: str = "/api/v1"

    class Config:
        case_sensitive = True

settings = Settings()