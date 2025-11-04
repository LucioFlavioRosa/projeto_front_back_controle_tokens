from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field

class TipoGraficoEnum(str, Enum):
    barras = 'barras'
    pizza = 'pizza'

class MetricaEnum(str, Enum):
    tokens_entrada = 'tokens_entrada'
    tokens_saida = 'tokens_saida'
    ambos = 'ambos'

class AgrupamentoEnum(str, Enum):
    projeto = 'projeto'
    tipo_analise = 'tipo_analise'
    usuario = 'usuario'
    modelo = 'modelo'
    dia = 'dia'

class QueryParams(BaseModel):
    data_inicio: datetime = Field(..., description="Data/hora inicial do período de análise.")
    data_fim: datetime = Field(..., description="Data/hora final do período de análise.")
    projetos: Optional[List[str]] = Field(None, description="Lista de projetos para filtrar.")
    usuarios: Optional[List[str]] = Field(None, description="Lista de usuários para filtrar.")
    tipos_analise: Optional[List[str]] = Field(None, description="Lista de tipos de análise para filtrar.")
    modelos_llm: Optional[List[str]] = Field(None, description="Lista de modelos LLM para filtrar.")
    tipo_grafico: TipoGraficoEnum = Field(..., description="Tipo de gráfico a ser plotado: barras ou pizza.")
    metrica: MetricaEnum = Field(..., description="Métrica a ser analisada: tokens_entrada, tokens_saida ou ambos.")
    agrupamento: AgrupamentoEnum = Field(..., description="Agrupamento dos dados: projeto, tipo_analise, usuario, modelo ou dia.")
