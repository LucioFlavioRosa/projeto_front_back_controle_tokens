from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

# Middleware de rate limiting para FastAPI
limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])


def register_rate_limit(app: FastAPI):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Limite de requisições atingido. Tente novamente em instantes.",
            "error": str(exc)
        }
    )

# Exemplo de uso no endpoint:
# from slowapi.decorator import limiter
# @app.get("/analytics")
# @limiter.limit("100/minute")
# async def analytics(...):
#     ...
