"""
Structured logging configuration
"""
import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured JSON logging"""
    
    # Create JSON formatter
    log_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    log_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(log_handler)
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Reduce noise from uvicorn
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name"""
    return logging.getLogger(name)
