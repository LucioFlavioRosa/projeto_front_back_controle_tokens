import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app.services.token_analytics_service import TokenAnalyticsService

MOCK_LOGS = [
    {
        'data_hora': datetime(2024, 6, 1, 12, 0),
        'projeto': 'Projeto A',
        'usuario_executor': 'user1',
        'tokens_entrada': 100,
        'tokens_saida': 80,
        'tipo_analise': 'analise1',
        'model_name': 'gpt-4',
    },
    {
        'data_hora': datetime(2024, 6, 2, 13, 0),
        'projeto': 'Projeto B',
        'usuario_executor': 'user2',
        'tokens_entrada': 200,
        'tokens_saida': 180,
        'tipo_analise': 'analise2',
        'model_name': 'gpt-3',
    },
    {
        'data_hora': datetime(2024, 6, 1, 14, 0),
        'projeto': 'Projeto A',
        'usuario_executor': 'user1',
        'tokens_entrada': 50,
        'tokens_saida': 40,
        'tipo_analise': 'analise1',
        'model_name': 'gpt-4',
    },
]

def test_build_filters_by_projeto():
    service = TokenAnalyticsService(MOCK_LOGS)
    filters = {'projeto': 'Projeto A'}
    filtered = service._build_filters(MOCK_LOGS, filters)
    assert all(e['projeto'] == 'Projeto A' for e in filtered)
    assert len(filtered) == 2

def test_group_and_summarize_by_projeto():
    service = TokenAnalyticsService(MOCK_LOGS)
    group_by = ['projeto']
    sum_fields = ['tokens_entrada', 'tokens_saida']
    result = service._group_and_summarize(MOCK_LOGS, group_by, sum_fields)
    projetos = {r['projeto']: r for r in result}
    assert projetos['Projeto A']['tokens_entrada'] == 150
    assert projetos['Projeto B']['tokens_saida'] == 180

def test_tokens_by_project():
    service = TokenAnalyticsService(MOCK_LOGS)
    filters = {}
    result = service.tokens_by_project(filters)
    assert any(r['projeto'] == 'Projeto A' for r in result)
    assert any(r['projeto'] == 'Projeto B' for r in result)

def test_tokens_by_project_group_by_user():
    service = TokenAnalyticsService(MOCK_LOGS)
    filters = {}
    result = service.tokens_by_project(filters, group_by_user=True)
    for r in result:
        assert 'usuario_executor' in r

def test_tokens_by_tipo_analise():
    service = TokenAnalyticsService(MOCK_LOGS)
    filters = {}
    result = service.tokens_by_tipo_analise(filters)
    tipos = {r['tipo_analise']: r for r in result}
    assert tipos['analise1']['tokens_entrada'] == 150
    assert tipos['analise2']['tokens_saida'] == 180

def test_tokens_by_day():
    service = TokenAnalyticsService(MOCK_LOGS)
    filters = {}
    result = service.tokens_by_day(filters)
    dias = {r['dia']: r for r in result}
    assert dias['2024-06-01']['tokens_entrada'] == 150
    assert dias['2024-06-02']['tokens_saida'] == 180

def test_tokens_by_model():
    service = TokenAnalyticsService(MOCK_LOGS)
    filters = {}
    result = service.tokens_by_model(filters)
    models = {r['model_name']: r for r in result}
    assert models['gpt-4']['tokens_entrada'] == 150
    assert models['gpt-3']['tokens_saida'] == 180

def test_tokens_by_model_time():
    service = TokenAnalyticsService(MOCK_LOGS)
    filters = {}
    result = service.tokens_by_model_time(filters)
    for r in result:
        assert 'model_name' in r and 'dia' in r

def test_build_filters_with_date_range():
    service = TokenAnalyticsService(MOCK_LOGS)
    filters = {
        'data_inicio': datetime(2024, 6, 2, 0, 0),
        'data_fim': datetime(2024, 6, 2, 23, 59)
    }
    filtered = service._build_filters(MOCK_LOGS, filters)
    assert len(filtered) == 1
    assert filtered[0]['projeto'] == 'Projeto B'
