from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class TokenQueryRequest(BaseModel):
    data_inicio: datetime = Field(..., description="Data de início do período de análise")
    data_fim: datetime = Field(..., description="Data de fim do período de análise")
    projeto: Optional[str] = Field(None, description="Nome do projeto para filtrar")
    usuario_executor: Optional[str] = Field(None, description="Usuário executor para filtrar")
    tipo_analise: Optional[str] = Field(None, description="Tipo de análise para filtrar")
    model_name: Optional[str] = Field(None, description="Nome do modelo LLM para filtrar")
    agrupamento: Optional[List[str]] = Field(None, description="Campos para agrupamento dos dados, ex: ['projeto', 'usuario_executor']")

class TokenDataPoint(BaseModel):
    data_hora: Optional[datetime] = Field(None, description="Data/hora do ponto de dados")
    valor: float = Field(..., description="Valor do dado (ex: quantidade de tokens)")
    label: Optional[str] = Field(None, description="Rótulo do dado (ex: nome do projeto, tipo de análise, etc)")

class TokenAnalyticsResponse(BaseModel):
    dados: List[TokenDataPoint] = Field(..., description="Lista de pontos de dados para o gráfico")
    metadados: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais sobre a consulta ou agrupamento")
