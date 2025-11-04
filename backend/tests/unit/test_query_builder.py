import pytest
from datetime import datetime
from app.utils.query_builder import KQLQueryBuilder

def test_basic_where_filter():
    qb = KQLQueryBuilder('traces')
    qb.add_field_filter('projeto', 'ProjetoA')
    query = qb.build()
    assert "| where projeto == 'ProjetoA'" in query

def test_time_filter():
    start = datetime(2023, 1, 1, 0, 0, 0)
    end = datetime(2023, 1, 31, 23, 59, 59)
    qb = KQLQueryBuilder('traces')
    qb.add_time_filter('timestamp', start, end)
    query = qb.build()
    assert f"timestamp >= datetime('{start.isoformat()}') and timestamp <= datetime('{end.isoformat()}')" in query

def test_in_filter():
    qb = KQLQueryBuilder('traces')
    qb.add_in_filter('projeto', ['ProjetoA', 'ProjetoB'])
    query = qb.build()
    assert "projeto in ('ProjetoA', 'ProjetoB')" in query

def test_extend_and_aggregation():
    qb = KQLQueryBuilder('traces')
    qb.add_extend("msg_data = parse_json(message)")
    qb.add_aggregation("summarize avg(tokens_entrada) by projeto")
    query = qb.build()
    assert "| extend msg_data = parse_json(message)" in query
    assert "| summarize avg(tokens_entrada) by projeto" in query

def test_summarize_and_order_by():
    qb = KQLQueryBuilder('traces')
    qb.set_summarize("Media_Tokens_Entrada = avg(tokens_entrada) by projeto, usuario_executor")
    qb.set_order_by("projeto asc, Media_Tokens_Entrada desc")
    query = qb.build()
    assert "| summarize Media_Tokens_Entrada = avg(tokens_entrada) by projeto, usuario_executor" in query
    assert "| order by projeto asc, Media_Tokens_Entrada desc" in query
