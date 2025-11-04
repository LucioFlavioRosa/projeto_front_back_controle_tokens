from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import logging

from app.services.query_builder_service import QueryBuilderService
from app.services.data_aggregation_service import DataAggregationService
# from app.services.azure_insights_service import AzureInsightsService  # Supondo implementação já existente

router = APIRouter()

class QueryRequest(BaseModel):
    tipo_grafico: str  # 'bar' ou 'pie'
    tipo_consulta: str  # 'projeto', 'agente', 'periodo', 'modelo'
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    usuario: Optional[str] = None
    projeto: Optional[str] = None
    model_name: Optional[str] = None
    periodo: Optional[str] = None  # 'day', 'hour', etc
    agrupamento_usuario: Optional[bool] = False
    tipo: Optional[str] = 'entrada'  # 'entrada' ou 'saida'

@router.post("/api/analytics/tokens")
async def token_analytics(request: Request, body: QueryRequest):
    try:
        qb = QueryBuilderService()
        # Escolha do método de query
        if body.tipo_consulta == 'projeto':
            kql = qb.build_tokens_by_project(
                start_date=body.start_date,
                end_date=body.end_date,
                usuario=body.usuario,
                agrupamento_usuario=body.agrupamento_usuario
            )
            label_field = 'projeto'
            value_field = 'Total_Tokens_Entrada'
        elif body.tipo_consulta == 'agente':
            kql = qb.build_tokens_by_agent(
                start_date=body.start_date,
                end_date=body.end_date,
                projeto=body.projeto,
                agrupamento_usuario=body.agrupamento_usuario
            )
            label_field = 'usuario_executor'
            value_field = 'Total_Tokens_Entrada'
        elif body.tipo_consulta == 'periodo':
            kql = qb.build_tokens_by_period(
                start_date=body.start_date,
                end_date=body.end_date,
                periodo=body.periodo,
                projeto=body.projeto,
                usuario=body.usuario,
                tipo=body.tipo,
                agrupamento_usuario=body.agrupamento_usuario
            )
            label_field = 'bin_data_hora'
            value_field = 'Total_Tokens'
        elif body.tipo_consulta == 'modelo':
            kql = qb.build_tokens_by_model(
                start_date=body.start_date,
                end_date=body.end_date,
                periodo=body.periodo,
                agrupamento_usuario=body.agrupamento_usuario
            )
            label_field = 'model_name'
            value_field = 'Total_Tokens_Entrada'
        else:
            raise HTTPException(status_code=400, detail="tipo_consulta inválido")

        # Executa query no Azure Application Insights
        # azure_service = AzureInsightsService()
        # raw_data = azure_service.run_query(kql)
        # Para exemplo, simula resultado:
        raw_data = [
            {label_field: "Projeto A", value_field: 1234},
            {label_field: "Projeto B", value_field: 987},
            {label_field: "Projeto C", value_field: 456}
        ]

        # Agrega dados para Chart.js
        if body.tipo_grafico == 'bar':
            chart_data = DataAggregationService.aggregate_for_bar_chart(raw_data, label_field, value_field)
        elif body.tipo_grafico == 'pie':
            chart_data = DataAggregationService.aggregate_for_pie_chart(raw_data, label_field, value_field)
        else:
            raise HTTPException(status_code=400, detail="tipo_grafico inválido")

        return {"success": True, "chart": chart_data, "kql": kql}
    except Exception as e:
        logging.error(f"Erro ao processar analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
