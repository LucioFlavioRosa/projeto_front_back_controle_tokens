from fastapi.responses import JSONResponse
from fastapi import Request
from typing import Any, Dict


def handle_validation_error(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": str(exc),
                "details": {}
            }
        }
    )

def handle_azure_error(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "AZURE_ERROR",
                "message": str(exc),
                "details": {}
            }
        }
    )

def handle_generic_error(request: Request, exc: Exception) -> JSONResponse:
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
