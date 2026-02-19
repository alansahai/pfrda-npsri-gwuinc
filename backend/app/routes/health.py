"""
Health check and status endpoints
"""
from datetime import datetime
from fastapi import APIRouter

from app.core.config import settings
from app.models.schemas import HealthCheckResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify API is running
    
    Returns:
        HealthCheckResponse with status, version, and timestamp
    """
    return HealthCheckResponse(
        status="ok",
        version=settings.APP_VERSION,
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }
