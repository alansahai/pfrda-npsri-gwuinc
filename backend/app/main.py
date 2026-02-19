"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging_config import setup_logging, get_logger
from app.core.middleware import RequestLoggingMiddleware, ErrorHandlingMiddleware
from app.routes import health, forecast, projections

# Setup logging
setup_logging(log_level="INFO" if not settings.DEBUG else "DEBUG")
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info(
        f"Starting {settings.APP_NAME} v{settings.APP_VERSION}",
        extra={"debug_mode": settings.DEBUG}
    )
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.APP_NAME}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Predictive Pension Forecasting & Decision Support Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Add custom middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# Include routers
app.include_router(health.router)
app.include_router(forecast.router, prefix=settings.API_V1_PREFIX)
app.include_router(projections.router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
