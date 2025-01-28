from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "OneTap AI"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY")
    
    CORS_ORIGINS: list = ["http://localhost:52501"]
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()