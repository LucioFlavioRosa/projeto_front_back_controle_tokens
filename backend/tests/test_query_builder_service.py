import pytest
from backend.services.query_builder_service import QueryBuilderService

@pytest.fixture
def builder():
    return QueryBuilderService()

def test_build_tokens_by_project(builder):
    query = builder.build_query(aggregation='tokens_by_project', filters={})
    assert 'summarize' in query
    assert 'by projeto' in query
    assert 'tokens_entrada' in query or 'tokens_saida' in query

def test_build_tokens_by_agent(builder):
    query = builder.build_query(aggregation='tokens_by_agent', filters={})
    assert 'by usuario_executor' in query

def test_build_tokens_by_model(builder):
    query = builder.build_query(aggregation='tokens_by_model', filters={})
    assert 'by model_name' in query

def test_build_tokens_by_period(builder):
    query = builder.build_query(aggregation='tokens_by_period', filters={'start_date': '2024-06-01', 'end_date': '2024-06-10'})
    assert 'timestamp > datetime(2024-06-01)' in query
    assert 'timestamp < datetime(2024-06-10)' in query

def test_build_with_group_by_user(builder):
    query = builder.build_query(aggregation='tokens_by_project', filters={'group_by_user': True})
    assert 'by projeto, usuario_executor' in query

def test_invalid_aggregation(builder):
    with pytest.raises(ValueError):
        builder.build_query(aggregation='invalid_type', filters={})
