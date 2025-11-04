from typing import Optional, List
from datetime import datetime

class QueryBuilderService:
    """
    Serviço responsável por construir queries KQL dinâmicas para análise de tokens.
    """

    BASE_SELECT = "traces | extend msg_data = parse_json(message) | extend projeto = tostring(msg_data.projeto), usuario_executor = tostring(msg_data.usuario_executor), tokens_entrada = todouble(msg_data.tokens_entrada), tokens_saida = todouble(msg_data.tokens_saida), job_id = tostring(msg_data.job_id), model_name = tostring(msg_data.model_name), tipo_analise = tostring(msg_data.tipo_analise), data_hora = todatetime(msg_data.data_hora)"

    def _date_filter(self, start_date: Optional[str], end_date: Optional[str]) -> str:
        filters = []
        if start_date:
            filters.append(f"data_hora >= datetime({start_date})")
        if end_date:
            filters.append(f"data_hora <= datetime({end_date})")
        return " and ".join(filters) if filters else ""

    def _user_filter(self, usuario: Optional[str]) -> str:
        return f"usuario_executor == '{usuario}'" if usuario else ""

    def _project_filter(self, projeto: Optional[str]) -> str:
        return f"projeto == '{projeto}'" if projeto else ""

    def _model_filter(self, model_name: Optional[str]) -> str:
        return f"model_name == '{model_name}'" if model_name else ""

    def _compose_where(self, filters: List[str]) -> str:
        filters = [f for f in filters if f]
        return f"| where {' and '.join(filters)}" if filters else ""

    def build_tokens_by_project(self, start_date: Optional[str] = None, end_date: Optional[str] = None, usuario: Optional[str] = None, agrupamento_usuario: bool = False) -> str:
        filters = [self._date_filter(start_date, end_date), self._user_filter(usuario)]
        where_clause = self._compose_where(filters)
        group_by = "projeto, usuario_executor" if agrupamento_usuario else "projeto"
        query = f"{self.BASE_SELECT} {where_clause} | summarize Total_Tokens_Entrada = sum(tokens_entrada), Total_Tokens_Saida = sum(tokens_saida) by {group_by} | order by Total_Tokens_Entrada desc"
        return query

    def build_tokens_by_agent(self, start_date: Optional[str] = None, end_date: Optional[str] = None, projeto: Optional[str] = None, agrupamento_usuario: bool = False) -> str:
        filters = [self._date_filter(start_date, end_date), self._project_filter(projeto)]
        where_clause = self._compose_where(filters)
        group_by = "usuario_executor, projeto" if agrupamento_usuario else "usuario_executor"
        query = f"{self.BASE_SELECT} {where_clause} | summarize Total_Tokens_Entrada = sum(tokens_entrada), Total_Tokens_Saida = sum(tokens_saida) by {group_by} | order by Total_Tokens_Entrada desc"
        return query

    def build_tokens_by_period(self, start_date: Optional[str] = None, end_date: Optional[str] = None, periodo: str = 'day', projeto: Optional[str] = None, usuario: Optional[str] = None, tipo: str = 'entrada', agrupamento_usuario: bool = False) -> str:
        filters = [self._date_filter(start_date, end_date), self._project_filter(projeto), self._user_filter(usuario)]
        where_clause = self._compose_where(filters)
        token_field = 'tokens_entrada' if tipo == 'entrada' else 'tokens_saida'
        group_by = f"bin(data_hora, 1{periodo}), projeto, usuario_executor" if agrupamento_usuario else f"bin(data_hora, 1{periodo})"
        query = f"{self.BASE_SELECT} {where_clause} | summarize Total_Tokens = sum({token_field}) by {group_by} | order by bin_data_hora asc"
        return query

    def build_tokens_by_model(self, start_date: Optional[str] = None, end_date: Optional[str] = None, periodo: Optional[str] = None, agrupamento_usuario: bool = False) -> str:
        filters = [self._date_filter(start_date, end_date)]
        where_clause = self._compose_where(filters)
        if periodo:
            group_by = f"model_name, bin(data_hora, 1{periodo})"
        else:
            group_by = "model_name"
        if agrupamento_usuario:
            group_by += ", usuario_executor"
        query = f"{self.BASE_SELECT} {where_clause} | summarize Total_Tokens_Entrada = sum(tokens_entrada), Total_Tokens_Saida = sum(tokens_saida) by {group_by} | order by Total_Tokens_Entrada desc"
        return query
