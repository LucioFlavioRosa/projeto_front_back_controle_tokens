import os
from typing import List, Dict
from azure.monitor.query import LogsQueryClient
from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryStatus

class AzureInsightsService:
    def __init__(self):
        self.client_id = os.getenv('AZURE_CLIENT_ID')
        self.client_secret = os.getenv('AZURE_CLIENT_SECRET')
        self.tenant_id = os.getenv('AZURE_TENANT_ID')
        self.workspace_id = os.getenv('WORKSPACE_ID')
        if not all([self.client_id, self.client_secret, self.tenant_id, self.workspace_id]):
            raise EnvironmentError('Variáveis de ambiente AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID, WORKSPACE_ID devem estar definidas')
        self.credential = ClientSecretCredential(self.tenant_id, self.client_id, self.client_secret)
        self.client = LogsQueryClient(self.credential)

    def query_application_insights(self, query: str) -> List[Dict]:
        """
        Executa uma query KQL no Application Insights e retorna lista de dicts com os resultados.
        """
        response = self.client.query_workspace(
            workspace_id=self.workspace_id,
            query=query
        )
        if response.status == LogsQueryStatus.PARTIAL:
            # Pode retornar resultados parciais
            main_table = response.partial_data[0] if response.partial_data else None
        elif response.status == LogsQueryStatus.SUCCESS:
            main_table = response.tables[0] if response.tables else None
        else:
            raise Exception(f'Erro ao consultar Application Insights: {response.status}')

        results = []
        if main_table:
            columns = [col.name for col in main_table.columns]
            for row in main_table.rows:
                results.append({col: row[idx] for idx, col in enumerate(columns)})
        return results
