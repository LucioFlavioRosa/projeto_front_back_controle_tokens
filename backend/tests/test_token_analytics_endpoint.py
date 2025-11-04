import pytest
from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture
def valid_request():
    return {
        "aggregation": "tokens_by_project",
        "filters": {
            "start_date": "2024-06-01",
            "end_date": "2024-06-10",
            "group_by_user": True
        }
    }

def test_analytics_tokens_success(valid_request):
    response = client.post("/api/analytics/tokens", json=valid_request)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert 'result' in data
    assert isinstance(data['result'], list)

def test_analytics_tokens_invalid_dates():
    bad_request = {
        "aggregation": "tokens_by_project",
        "filters": {
            "start_date": "invalid-date",
            "end_date": "2024-06-10"
        }
    }
    response = client.post("/api/analytics/tokens", json=bad_request)
    assert response.status_code == 400 or response.status_code == 422

def test_analytics_tokens_workspace_not_found():
    request = {
        "aggregation": "tokens_by_project",
        "filters": {},
        "workspace_id": "wrong-workspace"
    }
    response = client.post("/api/analytics/tokens", json=request)
    assert response.status_code == 404 or response.status_code == 400

def test_analytics_tokens_invalid_aggregation():
    request = {
        "aggregation": "invalid_type",
        "filters": {}
    }
    response = client.post("/api/analytics/tokens", json=request)
    assert response.status_code == 400 or response.status_code == 422
