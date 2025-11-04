from fastapi import APIRouter
from .endpoints import token_analytics

api_router = APIRouter()
api_router.include_router(token_analytics.router, prefix="", tags=["Token Analytics"])
