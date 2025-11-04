from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional

class TokenMetrics(BaseModel):
    data_hora: datetime = Field(..., description="Data e hora do registro")
    job_id: str = Field(..., min_length=1, description="ID do job/processo")
    model_name: str = Field(..., min_length=1, description="Nome do modelo LLM")
    projeto: str = Field(..., min_length=1, description="Nome do projeto")
    tipo_analise: str = Field(..., min_length=1, description="Tipo de análise executada")
    tokens_entrada: int = Field(..., ge=0, description="Quantidade de tokens de entrada")
    tokens_saida: int = Field(..., ge=0, description="Quantidade de tokens de saída")
    usuario_executor: str = Field(..., min_length=1, description="Usuário executor da ação")

    @validator('data_hora')
    def validate_data_hora(cls, v):
        if not isinstance(v, datetime):
            raise ValueError('data_hora deve ser datetime')
        return v

    @validator('tokens_entrada', 'tokens_saida')
    def validate_tokens(cls, v):
        if v < 0:
            raise ValueError('Tokens não podem ser negativos')
        return v
