from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient
from azure.monitor.query import LogsQueryStatus
import os

class AzureInsightsService:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, workspace_id: str):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.workspace_id = workspace_id
        self.credential = None
        self.client = None

    def authenticate(self):
        self.credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.client = LogsQueryClient(self.credential)

    def execute_query(self, query: str, timespan=None):
        if self.client is None:
            self.authenticate()
        response = self.client.query_workspace(
            workspace_id=self.workspace_id,
            query=query,
            timespan=timespan
        )
        if response.status == LogsQueryStatus.PARTIAL:
            raise Exception(f"Query retornou apenas resultados parciais: {response.partial_error}")
        elif response.status == LogsQueryStatus.FAILURE:
            raise Exception(f"Erro na consulta ao Application Insights: {response.error}")
        return response.tables[0].rows if response.tables else []
