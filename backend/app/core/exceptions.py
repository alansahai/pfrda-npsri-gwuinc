"""
Custom exceptions for the application
"""
from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception"""
    
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(AppException):
    """Raised when input validation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class CalculationException(AppException):
    """Raised when calculation or simulation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)


class ResourceNotFoundException(AppException):
    """Raised when a requested resource is not found"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, status_code=404, details=details)
