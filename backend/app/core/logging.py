"""
Logging Configuration Module
Sets up structured logging for the application
"""
import logging
import sys
from typing import Any, Dict
from datetime import datetime
from app.core.config import settings


class StructuredFormatter(logging.Formatter):
    """Custom formatter for structured logging output"""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON-like output"""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
            
        # Format as key=value pairs for readability
        formatted_parts = [f"{k}={v}" for k, v in log_data.items()]
        return " | ".join(formatted_parts)


def setup_logging() -> None:
    """Configure application-wide logging"""
    
    # Get log level from settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Set formatter
    formatter = StructuredFormatter()
    console_handler.setFormatter(formatter)
    
    # Add handler to root logger
    root_logger.addHandler(console_handler)
    
    # Configure uvicorn loggers
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.handlers = [console_handler]
    
    uvicorn_error = logging.getLogger("uvicorn.error")
    uvicorn_error.handlers = [console_handler]
    
    # Log startup message
    logging.info(
        f"Logging configured - Level: {settings.LOG_LEVEL}, Environment: {settings.ENVIRONMENT}"
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name"""
    return logging.getLogger(name)
