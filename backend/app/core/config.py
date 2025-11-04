from pydantic import BaseSettings, AnyHttpUrl, validator
from typing import List, Optional
import os

class Settings(BaseSettings):
    AZURE_TENANT_ID: str
    AZURE_CLIENT_ID: str
    AZURE_CLIENT_SECRET: str
    AZURE_WORKSPACE_ID: str
    CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        env_file = os.getenv('ENV_FILE', '.env')
        case_sensitive = True

    @validator('CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(',') if i.strip()]
        elif isinstance(v, list):
            return v
        return []

settings = Settings()
