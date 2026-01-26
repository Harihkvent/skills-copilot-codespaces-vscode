"""
Core configuration module
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql://astra:astra_password@postgres:5432/astra_db"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # SMTP Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM: Optional[str] = None
    
    # LLM Provider
    LLM_PROVIDER: str = "local"  # local or krutrim
    KRUTRIM_API_KEY: Optional[str] = None
    KRUTRIM_API_URL: Optional[str] = None
    
    # Local LLM
    LOCAL_LLM_MODEL: str = "llama2"
    LOCAL_LLM_URL: str = "http://localhost:11434"
    
    # STT Configuration
    STT_MODEL: str = "whisper"
    WHISPER_MODEL_SIZE: str = "base"
    
    # TTS Configuration
    TTS_ENGINE: str = "coqui"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
