from typing import List
from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Management API"
    API_V1_STR: str = "/api"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: PostgresDsn
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Debug mode
    DEBUG: bool = False
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 