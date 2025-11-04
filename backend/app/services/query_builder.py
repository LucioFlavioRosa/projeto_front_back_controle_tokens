from typing import Optional
from app.models.query_params import QueryParams

class QueryBuilder:
    @staticmethod
    def build_base_query(params: QueryParams) -> str:
        base = [
            "traces",
            f"| where timestamp >= datetime({params.data_inicio.isoformat()}) and timestamp <= datetime({params.data_fim.isoformat()})",
            "| extend msg_data = parse_json(message)",
            "| extend",
            "    data_hora = todatetime(msg_data.data_hora),",
            "    job_id = tostring(msg_data.job_id),",
            "    model_name = tostring(msg_data.model_name),",
            "    projeto = tostring(msg_data.projeto),",
            "    tipo_analise = tostring(msg_data.tipo_analise),",
            "    tokens_entrada = todouble(msg_data.tokens_entrada),",
            "    tokens_saida = todouble(msg_data.tokens_saida),",
            "    usuario_executor = tostring(msg_data.usuario_executor)"
        ]
        return '\n'.join(base)

    @staticmethod
    def add_filters(query: str, params: QueryParams) -> str:
        filters = []
        if params.projetos:
            projetos_str = ', '.join([f'\"{p}\"' for p in params.projetos])
            filters.append(f"projeto in ({projetos_str})")
        if params.usuarios:
            usuarios_str = ', '.join([f'\"{u}\"' for u in params.usuarios])
            filters.append(f"usuario_executor in ({usuarios_str})")
        if params.tipos_analise:
            tipos_str = ', '.join([f'\"{t}\"' for t in params.tipos_analise])
            filters.append(f"tipo_analise in ({tipos_str})")
        if params.modelos_llm:
            modelos_str = ', '.join([f'\"{m}\"' for m in params.modelos_llm])
            filters.append(f"model_name in ({modelos_str})")
        if filters:
            query += f"\n| where {' and '.join(filters)}"
        return query

    @staticmethod
    def add_aggregation(query: str, params: QueryParams) -> str:
        # Mapeamento dos campos de agrupamento
        agrupamentos = {
            'projeto': 'projeto',
            'tipo_analise': 'tipo_analise',
            'usuario': 'usuario_executor',
            'modelo': 'model_name',
            'dia': 'format_datetime(timestamp, \"yyyy-MM-dd\")'
        }
        group_field = agrupamentos.get(params.agrupamento)
        metrics = []
        if params.metrica == 'tokens_entrada':
            metrics.append('sum(tokens_entrada) as total_tokens_entrada')
        elif params.metrica == 'tokens_saida':
            metrics.append('sum(tokens_saida) as total_tokens_saida')
        elif params.metrica == 'ambos':
            metrics.append('sum(tokens_entrada) as total_tokens_entrada')
            metrics.append('sum(tokens_saida) as total_tokens_saida')
        # Suporte a agrupamento extra (exemplo: por usuário)
        if hasattr(params, 'agrupamento_extra') and params.agrupamento_extra:
            extra_field = agrupamentos.get(params.agrupamento_extra)
            group_by = f"{group_field}, {extra_field}"
        else:
            group_by = group_field
        query += f"\n| summarize {', '.join(metrics)} by {group_by}"
        query += f"\n| order by {group_by} asc"
        return query

    @staticmethod
    def build_query(params: QueryParams) -> str:
        query = QueryBuilder.build_base_query(params)
        query = QueryBuilder.add_filters(query, params)
        query = QueryBuilder.add_aggregation(query, params)
        return query
