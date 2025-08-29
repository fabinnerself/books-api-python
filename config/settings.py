"""
Configuration settings for the Books API
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file (only in development)
if os.getenv("APP_ENV") != "production":
    load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    # Database configuration
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "library")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "1")
    DB_SSLMODE: str = os.getenv("DB_SSLMODE", "disable")
    
    # Application configuration
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    APP_PORT: int = int(os.getenv("PORT", os.getenv("APP_PORT", "8000")))
    
    @property
    def database_url(self) -> str:
        """Construct database URL for SQLAlchemy"""
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    @property
    def database_url_sync(self) -> str:
        """Construct synchronous database URL for migrations"""
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.APP_ENV == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.APP_ENV == "development"

# Global settings instance
settings = Settings()