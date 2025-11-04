from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

router = APIRouter()

class CustomAnalyticsQuery(BaseModel):
    # Payload flexível para permitir evolução dos gráficos
    chart_type: str = Field(..., description="Tipo de gráfico a ser gerado, ex: 'bar', 'pie'")
    group_by: list[str] = Field(..., description="Lista de campos para agrupamento, ex: ['projeto', 'usuario_executor']")
    metric: str = Field(..., description="Campo métrico a ser analisado, ex: 'tokens_entrada', 'tokens_saida'")
    aggregation: str = Field(..., description="Tipo de agregação, ex: 'sum', 'avg', 'count'")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Filtros opcionais para a consulta, ex: {'projeto': 'Projeto X'}")
    period: Optional[Dict[str, str]] = Field(default=None, description="Intervalo de datas, ex: {'from': '2024-06-01', 'to': '2024-06-20'}")
    user_grouping: Optional[bool] = Field(default=False, description="Se deve agrupar por usuário também")
    # Campos adicionais podem ser enviados e ignorados pelo backend

@router.post("/analytics/custom-query")
async def custom_analytics_query(payload: CustomAnalyticsQuery, request: Request):
    """
    Endpoint genérico para consultas analíticas de tokens.
    Recebe um payload flexível e retorna os dados prontos para o frontend plotar gráficos.
    """
    # Simulação de consulta aos logs (Azure Application Insights, etc)
    # Aqui apenas retornamos o payload recebido e um exemplo de estrutura de dados
    # Em produção, implementar a consulta real ao backend/logs
    # O frontend é responsável por plotar os dados
    try:
        # Exemplo de resposta simulada (mock)
        data = {
            "labels": ["Projeto A", "Projeto B", "Projeto C"],
            "values": [12345, 6789, 2345],
            "grouped_by": payload.group_by,
            "metric": payload.metric,
            "aggregation": payload.aggregation,
            "filters": payload.filters,
            "period": payload.period,
            "chart_type": payload.chart_type,
            "user_grouping": payload.user_grouping
        }
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar consulta analítica: {str(e)}")
