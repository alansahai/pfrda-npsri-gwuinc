"""
Custom middleware for error handling and logging
"""
import time
import uuid
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging_config import get_logger
from app.core.exceptions import AppException

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all incoming requests and responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Log request
        start_time = time.time()
        logger.info(
            "Incoming request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client": request.client.host if request.client else None,
            }
        )
        
        # Process request
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            "Request completed",
            extra={
                "request_id": request_id,
                "status_code": response.status_code,
                "process_time_ms": round(process_time * 1000, 2),
            }
        )
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions and return proper error responses"""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except AppException as e:
            # Handle custom application exceptions
            logger.error(
                f"Application error: {e.message}",
                extra={
                    "request_id": getattr(request.state, "request_id", None),
                    "status_code": e.status_code,
                    "details": e.details,
                },
                exc_info=True
            )
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "detail": e.message,
                    "details": e.details,
                    "request_id": getattr(request.state, "request_id", None),
                }
            )
        except Exception as e:
            # Handle unexpected exceptions
            logger.error(
                f"Unexpected error: {str(e)}",
                extra={
                    "request_id": getattr(request.state, "request_id", None),
                },
                exc_info=True
            )
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Internal server error",
                    "request_id": getattr(request.state, "request_id", None),
                }
            )
