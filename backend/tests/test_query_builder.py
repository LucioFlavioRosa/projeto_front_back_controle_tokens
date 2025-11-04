import pytest
from unittest.mock import patch

# Supondo que QueryBuilder está em backend/app/services/query_builder.py
from app.services.query_builder import QueryBuilder

@pytest.fixture
def query_builder():
    return QueryBuilder()

def test_build_query_tokens_por_projeto(query_builder):
    query = query_builder.build_query(agrupamento="projeto", tipo_token="entrada")
    assert "projeto" in query
    assert "tokens_entrada" in query

def test_build_query_tokens_por_tipo_analise(query_builder):
    query = query_builder.build_query(agrupamento="tipo_analise", tipo_token="saida")
    assert "tipo_analise" in query
    assert "tokens_saida" in query

def test_build_query_tokens_por_dia(query_builder):
    query = query_builder.build_query(agrupamento="data_hora", tipo_token="entrada", periodo="7d")
    assert "data_hora" in query or "timestamp" in query
    assert "tokens_entrada" in query
    assert "ago(7d)" in query

def test_build_query_tokens_por_modelo(query_builder):
    query = query_builder.build_query(agrupamento="model_name", tipo_token="entrada")
    assert "model_name" in query
    assert "tokens_entrada" in query

def test_build_query_with_filters(query_builder):
    filters = {"projeto": "ProjetoX", "usuario_executor": "user1"}
    query = query_builder.build_query(agrupamento="projeto", tipo_token="saida", filtros=filters)
    assert "ProjetoX" in query
    assert "user1" in query
    assert "tokens_saida" in query
