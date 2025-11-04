import pytest
from app.services.data_processor import DataProcessor

@pytest.fixture
def processor():
    return DataProcessor()

def test_process_results_barras(processor):
    mock_data = [
        {"projeto": "A", "tokens_entrada": 100},
        {"projeto": "B", "tokens_entrada": 200}
    ]
    result = processor.process_results(mock_data, tipo_grafico="barras", agrupamento="projeto", tipo_token="entrada")
    assert isinstance(result, dict)
    assert "labels" in result and "values" in result
    assert result["labels"] == ["A", "B"]
    assert result["values"] == [100, 200]

def test_process_results_pizza(processor):
    mock_data = [
        {"tipo_analise": "analise1", "tokens_saida": 50},
        {"tipo_analise": "analise2", "tokens_saida": 150}
    ]
    result = processor.process_results(mock_data, tipo_grafico="pizza", agrupamento="tipo_analise", tipo_token="saida")
    assert isinstance(result, dict)
    assert "labels" in result and "values" in result
    assert result["labels"] == ["analise1", "analise2"]
    assert result["values"] == [50, 150]

def test_process_results_empty(processor):
    mock_data = []
    result = processor.process_results(mock_data, tipo_grafico="barras", agrupamento="projeto", tipo_token="entrada")
    assert result == {"labels": [], "values": []}

def test_process_results_multiple_datasets(processor):
    mock_data = [
        {"projeto": "A", "tokens_entrada": 100, "usuario_executor": "user1"},
        {"projeto": "A", "tokens_entrada": 150, "usuario_executor": "user2"},
        {"projeto": "B", "tokens_entrada": 200, "usuario_executor": "user1"}
    ]
    result = processor.process_results(mock_data, tipo_grafico="barras", agrupamento=["projeto", "usuario_executor"], tipo_token="entrada")
    assert isinstance(result, dict)
    assert "labels" in result and "values" in result
    assert ("A - user1" in result["labels"] or "A/user1" in result["labels"])
    assert len(result["labels"]) == 3
    assert len(result["values"]) == 3
