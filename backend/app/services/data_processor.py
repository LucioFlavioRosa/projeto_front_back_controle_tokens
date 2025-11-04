from typing import Any, Dict, List

class DataProcessor:
    @staticmethod
    def process_query_results(results: List[Dict[str, Any]], params) -> Dict[str, Any]:
        """
        Transforma os resultados brutos do Azure Application Insights em estrutura padronizada
        para o frontend: {"labels": [], "datasets": [{"label": "", "data": []}], "metadata": {}}
        """
        # Exemplo de params: params.grafico, params.agrupamento, params.metricas, etc.
        # O frontend pode pedir agrupamento por projeto, usuario, tipo_analise, modelo, etc.
        # O resultado do Azure já deve vir agrupado conforme a query construída.
        
        labels = []
        data = []
        dataset_label = params.metricas[0] if hasattr(params, 'metricas') and params.metricas else "valor"
        metadata = {}

        # Suporte a agrupamentos múltiplos (ex: por usuario + tipo_analise)
        if results and isinstance(results[0], dict):
            # Descobre as chaves de agrupamento (exceto as métricas)
            metric_keys = set(params.metricas) if hasattr(params, 'metricas') else set()
            group_keys = [k for k in results[0].keys() if k not in metric_keys]

            # Se for agrupamento simples (um eixo)
            if len(group_keys) == 1:
                labels = [row[group_keys[0]] for row in results]
                data = [row[dataset_label] for row in results]
                datasets = [{"label": dataset_label, "data": data}]
            # Se for agrupamento duplo (ex: por usuario e tipo_analise)
            elif len(group_keys) == 2:
                # Agrupa por eixo 1, e para cada um, cria um dataset para eixo 2
                eixo1 = group_keys[0]
                eixo2 = group_keys[1]
                eixo1_labels = sorted(list(set(row[eixo1] for row in results)))
                eixo2_labels = sorted(list(set(row[eixo2] for row in results)))
                labels = eixo1_labels
                datasets = []
                for e2 in eixo2_labels:
                    data = []
                    for e1 in eixo1_labels:
                        found = next((row for row in results if row[eixo1]==e1 and row[eixo2]==e2), None)
                        data.append(found[dataset_label] if found else 0)
                    datasets.append({"label": str(e2), "data": data})
                metadata = {"eixo1": eixo1, "eixo2": eixo2}
            else:
                # Mais de 2 agrupamentos: retorna tudo como metadados
                labels = []
                datasets = []
                metadata = {"raw": results}
        else:
            labels = []
            datasets = []
            metadata = {"raw": results}

        return {
            "labels": labels,
            "datasets": datasets,
            "metadata": metadata
        }
