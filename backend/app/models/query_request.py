from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

class QueryType(str, Enum):
    projeto = "projeto"
    agente = "agente"
    periodo = "periodo"
    modelo = "modelo"

class ChartType(str, Enum):
    bar = "bar"
    pie = "pie"

class QueryRequest(BaseModel):
    query_type: QueryType = Field(..., description="Tipo de consulta: projeto, agente, periodo, modelo")
    group_by: Optional[str] = Field(None, description="Agrupamento opcional, ex: usuario")
    start_date: datetime = Field(..., description="Data inicial do período")
    end_date: datetime = Field(..., description="Data final do período")
    chart_type: ChartType = Field(..., description="Tipo de gráfico: bar ou pie")
    filters: Optional[Dict[str, Any]] = Field(None, description="Filtros opcionais, ex: projeto, usuario, modelo")

    @validator('start_date', 'end_date')
    def validate_dates(cls, v):
        if not isinstance(v, datetime):
            raise ValueError('start_date e end_date devem ser datetime')
        return v

    @validator('group_by')
    def validate_group_by(cls, v):
        if v is not None and v != "usuario":
            raise ValueError('group_by só pode ser "usuario" ou None')
        return v
