from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient
from typing import Any, Dict
import os

class AzureInsightsClient:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, workspace_id: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.workspace_id = workspace_id
        self.credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.client = LogsQueryClient(self.credential)

    def execute_query(self, query: str) -> Dict[str, Any]:
        """
        Executa uma query KQL no Azure Application Insights e retorna os resultados.
        """
        response = self.client.query_workspace(
            workspace_id=self.workspace_id,
            query=query
        )
        if response.status != 'Success':
            raise Exception(f"Erro ao executar query no Application Insights: {response.status}")
        return response.tables[0].rows if response.tables else []
