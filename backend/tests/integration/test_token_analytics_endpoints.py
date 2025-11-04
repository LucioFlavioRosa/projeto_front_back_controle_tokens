import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

MOCK_ANALYTICS_DATA = {
    "labels": ["Projeto A", "Projeto B"],
    "values": [123, 456],
    "grouped_by": ["projeto"],
    "metric": "tokens_entrada",
    "aggregation": "sum",
    "filters": None,
    "period": None,
    "chart_type": "bar",
    "user_grouping": False
}

@patch("app.api.v1.endpoints.token_analytics.CustomAnalyticsQuery", autospec=True)
def test_custom_analytics_query_success(mock_query):
    payload = {
        "chart_type": "bar",
        "group_by": ["projeto"],
        "metric": "tokens_entrada",
        "aggregation": "sum",
        "filters": {},
        "period": {"from": "2024-06-01", "to": "2024-06-20"},
        "user_grouping": False
    }
    response = client.post("/v1/analytics/custom-query", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "data" in data
    assert "labels" in data["data"]
    assert "values" in data["data"]

@patch("app.api.v1.endpoints.token_analytics.CustomAnalyticsQuery", autospec=True)
def test_custom_analytics_query_invalid_payload(mock_query):
    payload = {
        # missing required fields
        "aggregation": "sum"
    }
    response = client.post("/v1/analytics/custom-query", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

@patch("app.api.v1.endpoints.token_analytics.CustomAnalyticsQuery", autospec=True)
def test_custom_analytics_query_internal_error(mock_query):
    with patch("app.api.v1.endpoints.token_analytics.custom_analytics_query", side_effect=Exception("fail")):
        payload = {
            "chart_type": "bar",
            "group_by": ["projeto"],
            "metric": "tokens_entrada",
            "aggregation": "sum",
            "filters": {},
            "period": {"from": "2024-06-01", "to": "2024-06-20"},
            "user_grouping": False
        }
        response = client.post("/v1/analytics/custom-query", json=payload)
        assert response.status_code == 500
        data = response.json()
        assert data["success"] is False or "Erro" in data["detail"]
