import pytest
from unittest.mock import patch, MagicMock
from backend.services.azure_insights_service import AzureInsightsService
from azure.monitor.query import LogsQueryStatus

@pytest.fixture
def mock_client():
    with patch('backend.services.azure_insights_service.LogsQueryClient') as MockClient:
        yield MockClient

@pytest.fixture
def service():
    return AzureInsightsService(workspace_id='test-workspace', credential='fake-cred')

@pytest.mark.parametrize('query,expected', [
    ("traces | where timestamp > ago(1d)", True),
    ("", False),
])
def test_validate_kql_query(service, query, expected):
    assert service.validate_kql_query(query) == expected

def test_run_query_success(mock_client, service):
    mock_instance = MagicMock()
    mock_instance.query_workspace.return_value.status = LogsQueryStatus.SUCCESS
    mock_instance.query_workspace.return_value.tables = [MagicMock(rows=[{'projeto': 'A', 'tokens_entrada': 100}])]
    mock_client.return_value = mock_instance
    result = service.run_query("traces | where timestamp > ago(1d)")
    assert isinstance(result, list)
    assert result[0]['projeto'] == 'A'
    assert result[0]['tokens_entrada'] == 100

def test_run_query_auth_error(mock_client, service):
    mock_instance = MagicMock()
    mock_instance.query_workspace.side_effect = Exception("Authentication failed")
    mock_client.return_value = mock_instance
    with pytest.raises(Exception) as exc:
        service.run_query("traces | where timestamp > ago(1d)")
    assert "Authentication failed" in str(exc.value)

def test_run_query_invalid_query(mock_client, service):
    with pytest.raises(ValueError):
        service.run_query("")
