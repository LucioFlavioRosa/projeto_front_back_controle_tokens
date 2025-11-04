from typing import Optional
from backend.app.models.query_params import QueryParams, AgrupamentoEnum, MetricaEnum

class QueryBuilder:
    @staticmethod
    def build_base_query(params: QueryParams) -> str:
        base = (
            "traces\n"
            f"| where timestamp >= datetime({params.data_inicio.isoformat()}) and timestamp <= datetime({params.data_fim.isoformat()})\n"
            "| extend msg_data = parse_json(message)\n"
            "| extend "
            "data_hora = tostring(msg_data.data_hora), "
            "job_id = tostring(msg_data.job_id), "
            "model_name = tostring(msg_data.model_name), "
            "projeto = tostring(msg_data.projeto), "
            "tipo_analise = tostring(msg_data.tipo_analise), "
            "tokens_entrada = todouble(msg_data.tokens_entrada), "
            "tokens_saida = todouble(msg_data.tokens_saida), "
            "usuario_executor = tostring(msg_data.usuario_executor)\n"
        )
        return base

    @staticmethod
    def add_filters(query: str, params: QueryParams) -> str:
        filters = []
        if params.projetos:
            projetos = ','.join([f"'{p}'" for p in params.projetos])
            filters.append(f"projeto in ({projetos})")
        if params.usuarios:
            usuarios = ','.join([f"'{u}'" for u in params.usuarios])
            filters.append(f"usuario_executor in ({usuarios})")
        if params.tipos_analise:
            tipos = ','.join([f"'{t}'" for t in params.tipos_analise])
            filters.append(f"tipo_analise in ({tipos})")
        if params.modelos_llm:
            modelos = ','.join([f"'{m}'" for m in params.modelos_llm])
            filters.append(f"model_name in ({modelos})")
        if filters:
            query += f"| where {' and '.join(filters)}\n"
        return query

    @staticmethod
    def add_aggregation(query: str, params: QueryParams) -> str:
        agrupamento_map = {
            AgrupamentoEnum.projeto: 'projeto',
            AgrupamentoEnum.tipo_analise: 'tipo_analise',
            AgrupamentoEnum.usuario: 'usuario_executor',
            AgrupamentoEnum.modelo: 'model_name',
            AgrupamentoEnum.dia: 'format_datetime(timestamp, \'yyyy-MM-dd\')',
        }
        group_by = agrupamento_map.get(params.agrupamento, 'projeto')
        metricas = []
        if params.metrica == MetricaEnum.tokens_entrada:
            metricas.append('sum(tokens_entrada) as Total_Tokens_Entrada')
        elif params.metrica == MetricaEnum.tokens_saida:
            metricas.append('sum(tokens_saida) as Total_Tokens_Saida')
        elif params.metrica == MetricaEnum.ambos:
            metricas.append('sum(tokens_entrada) as Total_Tokens_Entrada')
            metricas.append('sum(tokens_saida) as Total_Tokens_Saida')
        metricas_str = ', '.join(metricas)
        query += f"| summarize {metricas_str} by {group_by}\n"
        query += f"| order by {group_by} asc\n"
        return query

    @staticmethod
    def build_query(params: QueryParams) -> str:
        query = QueryBuilder.build_base_query(params)
        query = QueryBuilder.add_filters(query, params)
        query = QueryBuilder.add_aggregation(query, params)
        return query
