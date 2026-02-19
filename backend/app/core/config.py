"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "NPS Retirement Intelligence Engine"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    API_VERSION: str = "v1"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8080",
        "https://pfrda-npsri-gwuinc.vercel.app",  # Production frontend
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Simulation defaults
    MAX_SIMULATION_ITERATIONS: int = 10000
    DEFAULT_SIMULATION_ITERATIONS: int = 5000
    DEFAULT_MONTE_CARLO_ITERATIONS: int = 10000
    MAX_MONTE_CARLO_ITERATIONS: int = 50000
    
    # Risk scenario parameters (annual returns in %)
    CONSERVATIVE_RETURN_MIN: float = 4.0
    CONSERVATIVE_RETURN_MAX: float = 6.0
    MODERATE_RETURN_MIN: float = 6.0
    MODERATE_RETURN_MAX: float = 8.0
    AGGRESSIVE_RETURN_MIN: float = 8.0
    AGGRESSIVE_RETURN_MAX: float = 10.0
    
    # Annuity parameters
    DEFAULT_ANNUITY_RATE: float = 6.0  # Annual annuity rate %
    CORPUS_ANNUITY_ALLOCATION: float = 0.4  # 40% to annuity, 60% lump sum (standard NPS pattern)
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields from .env


# Global settings instance
settings = Settings()
