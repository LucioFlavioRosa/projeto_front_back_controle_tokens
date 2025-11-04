from typing import Any, Dict, List

class DataProcessor:
    @staticmethod
    def process_query_results(results: List[Dict[str, Any]], params) -> Dict[str, Any]:
        """
        Transforma os resultados brutos do Azure em estrutura JSON padronizada para o frontend.
        Espera-se que 'results' seja uma lista de dicionários (cada um representando uma linha do resultado da query).
        'params' é uma instância de QueryParams (ou similar) com os parâmetros da consulta.
        """
        labels = []
        datasets = []
        metadata = {}

        # Exemplo genérico: assume que há uma coluna 'label' e uma 'value' nos resultados
        # O processamento real pode ser ajustado conforme a query e os parâmetros
        if not results:
            return {"labels": [], "datasets": [{"label": "", "data": []}], "metadata": {}}

        # Determina dinamicamente as chaves relevantes
        # Exemplo: se params agrupa por 'projeto', busca essa coluna
        # Se múltiplos datasets (ex: por usuário), monta datasets múltiplos
        # Aqui, faz um processamento genérico e adaptável
        first_row = results[0]
        possible_label_keys = [
            'projeto', 'tipo_analise', 'usuario_executor', 'model_name', 'data_hora', 'dia', 'periodo'
        ]
        value_keys = [
            'tokens_entrada', 'tokens_saida', 'Media_Tokens_Entrada', 'Media_Tokens_Saida', 'total_tokens', 'count'
        ]

        label_key = next((k for k in possible_label_keys if k in first_row), None)
        value_key = next((k for k in value_keys if k in first_row), None)
        dataset_label = value_key if value_key else "valor"

        if label_key and value_key:
            labels = [str(row[label_key]) for row in results]
            data = [row[value_key] for row in results]
            datasets = [{"label": dataset_label, "data": data}]
        else:
            # fallback: retorna tudo como metadata
            metadata = {"raw": results}

        # Inclui metadados úteis (ex: parâmetros usados na consulta)
        metadata.update({
            "params": getattr(params, '__dict__', str(params))
        })

        return {
            "labels": labels,
            "datasets": datasets,
            "metadata": metadata
        }
