import pytest
from app.services.data_processor import DataProcessor

@pytest.fixture
def processor():
    return DataProcessor()

def test_process_results_barras(processor):
    # Simula dados de entrada para gráfico de barras
    raw_data = [
        {"projeto": "A", "tokens_entrada": 100},
        {"projeto": "B", "tokens_entrada": 200}
    ]
    output = processor.process_results(raw_data, chart_type="bar", group_by=["projeto"], metric="tokens_entrada")
    assert output["type"] == "bar"
    assert set(output["labels"]) == {"A", "B"}
    assert output["datasets"][0]["data"] == [100, 200]

def test_process_results_pizza(processor):
    raw_data = [
        {"tipo_analise": "static", "tokens_saida": 50},
        {"tipo_analise": "dynamic", "tokens_saida": 150}
    ]
    output = processor.process_results(raw_data, chart_type="pie", group_by=["tipo_analise"], metric="tokens_saida")
    assert output["type"] == "pie"
    assert set(output["labels"]) == {"static", "dynamic"}
    assert output["datasets"][0]["data"] == [50, 150]

def test_process_results_empty(processor):
    raw_data = []
    output = processor.process_results(raw_data, chart_type="bar", group_by=["projeto"], metric="tokens_entrada")
    assert output["labels"] == []
    assert output["datasets"][0]["data"] == []

def test_process_results_multiple_datasets(processor):
    # Simula agrupamento por dois campos
    raw_data = [
        {"projeto": "A", "usuario_executor": "u1", "tokens_entrada": 30},
        {"projeto": "A", "usuario_executor": "u2", "tokens_entrada": 70},
        {"projeto": "B", "usuario_executor": "u1", "tokens_entrada": 50}
    ]
    output = processor.process_results(
        raw_data,
        chart_type="bar",
        group_by=["projeto", "usuario_executor"],
        metric="tokens_entrada"
    )
    assert output["type"] == "bar"
    assert set(output["labels"]) == {"A", "B"}
    # Deve haver um dataset para cada usuario_executor
    usuarios = set(d["usuario_executor"] for d in raw_data)
    dataset_labels = set(ds["label"] for ds in output["datasets"])
    assert usuarios == dataset_labels
