import pytest
from unittest.mock import patch

# Supondo que QueryBuilder está em backend/app/services/query_builder.py
from app.services.query_builder import QueryBuilder

@pytest.fixture
def builder():
    return QueryBuilder()

def test_build_query_tokens_por_projeto(builder):
    query = builder.build_query(
        metric='tokens_entrada',
        group_by=['projeto'],
        filters={}
    )
    assert 'by projeto' in query
    assert 'tokens_entrada' in query

def test_build_query_tokens_por_tipo_analise(builder):
    query = builder.build_query(
        metric='tokens_saida',
        group_by=['tipo_analise'],
        filters={}
    )
    assert 'by tipo_analise' in query
    assert 'tokens_saida' in query

def test_build_query_tokens_por_dia(builder):
    query = builder.build_query(
        metric='tokens_entrada',
        group_by=['data_hora'],
        filters={}
    )
    assert 'by data_hora' in query
    assert 'tokens_entrada' in query

def test_build_query_tokens_por_modelo(builder):
    query = builder.build_query(
        metric='tokens_saida',
        group_by=['model_name'],
        filters={}
    )
    assert 'by model_name' in query
    assert 'tokens_saida' in query

def test_build_query_with_filters(builder):
    filters = {'projeto': 'ProjetoX', 'usuario_executor': 'user1'}
    query = builder.build_query(
        metric='tokens_entrada',
        group_by=['projeto', 'usuario_executor'],
        filters=filters
    )
    assert 'projeto == "ProjetoX"' in query or 'projeto == \'ProjetoX\'' in query
    assert 'usuario_executor == "user1"' in query or 'usuario_executor == \'user1\'' in query
    assert 'by projeto, usuario_executor' in query
