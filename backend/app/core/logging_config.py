import logging
import structlog
from fastapi import Request

# Configuração de logging estruturado (JSON) com structlog

def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        stream=None,
        level=logging.INFO
    )
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def bind_request_context(request: Request, user: str = None, job_id: str = None):
    # Adiciona contexto de requisição aos logs
    structlog.contextvars.bind_contextvars(
        user=user or getattr(request.state, "user", None),
        job_id=job_id or getattr(request.state, "job_id", None),
        path=request.url.path,
        method=request.method,
        client=str(request.client.host) if request.client else None
    )


def clear_request_context():
    structlog.contextvars.clear_contextvars()

# Exemplo de uso em endpoint:
# from .logging_config import bind_request_context, clear_request_context
# @app.middleware("http")
# async def log_context_middleware(request: Request, call_next):
#     bind_request_context(request)
#     response = await call_next(request)
#     clear_request_context()
#     return response

# logger = structlog.get_logger()
# logger.info("analytics_query", query="...", result_count=123)
