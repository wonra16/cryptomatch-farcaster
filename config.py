from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App Config
    app_name: str = "CryptoMatch"
    base_url: str = os.getenv("BASE_URL", "http://localhost:8000")
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # OpenAI
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Farcaster
    farcaster_hub_url: str = os.getenv("FARCASTER_HUB_URL", "https://hub.farcaster.xyz")
    
    # Rate Limiting
    rate_limit_per_user: int = int(os.getenv("RATE_LIMIT_PER_USER", "100"))
    cache_ttl: int = int(os.getenv("CACHE_TTL", "86400"))
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
