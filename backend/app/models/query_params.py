from typing import List, Optional, Literal
from datetime import datetime
from pydantic import BaseModel, Field, validator

class QueryParams(BaseModel):
    data_inicio: datetime = Field(..., description="Data/hora de início do período a consultar")
    data_fim: datetime = Field(..., description="Data/hora de fim do período a consultar")
    projetos: Optional[List[str]] = Field(None, description="Lista de projetos a filtrar")
    usuarios: Optional[List[str]] = Field(None, description="Lista de usuários a filtrar")
    tipos_analise: Optional[List[str]] = Field(None, description="Lista de tipos de análise a filtrar")
    modelos_llm: Optional[List[str]] = Field(None, description="Lista de modelos LLM a filtrar")
    tipo_grafico: Literal['barras', 'pizza'] = Field(..., description="Tipo de gráfico desejado")
    metrica: Literal['tokens_entrada', 'tokens_saida', 'ambos'] = Field(..., description="Métrica a ser analisada")
    agrupamento: Literal['projeto', 'tipo_analise', 'usuario', 'modelo', 'dia'] = Field(..., description="Campo de agrupamento principal")

    @validator('data_fim')
    def fim_maior_que_inicio(cls, v, values):
        if 'data_inicio' in values and v < values['data_inicio']:
            raise ValueError('data_fim deve ser maior ou igual a data_inicio')
        return v
