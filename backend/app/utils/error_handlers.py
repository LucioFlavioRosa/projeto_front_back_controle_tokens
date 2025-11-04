from fastapi.responses import JSONResponse
from fastapi import Request
from typing import Any, Dict

class AzureQueryError(Exception):
    def __init__(self, message: str, code: str = "AZURE_QUERY_ERROR", details: Dict[str, Any] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(Exception):
    def __init__(self, message: str, code: str = "VALIDATION_ERROR", details: Dict[str, Any] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

def handle_validation_error(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

def handle_azure_error(request: Request, exc: AzureQueryError):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

def handle_generic_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "GENERIC_ERROR",
                "message": str(exc),
                "details": {}
            }
        }
    )
