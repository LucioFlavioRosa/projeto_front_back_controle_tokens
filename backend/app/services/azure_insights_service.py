from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient
from azure.core.exceptions import HttpResponseError
import os

class AzureInsightsService:
    def __init__(self):
        self.credential = None
        self.client = None
        self.workspace_id = os.getenv('AZURE_APPINSIGHTS_WORKSPACE_ID')
        self.tenant_id = os.getenv('AZURE_TENANT_ID')
        self.client_id = os.getenv('AZURE_CLIENT_ID')
        self.client_secret = os.getenv('AZURE_CLIENT_SECRET')

    def authenticate(self):
        """
        Autentica via Service Principal usando ClientSecretCredential.
        """
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise ValueError("Credenciais do Azure não encontradas nas variáveis de ambiente.")
        self.credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.client = LogsQueryClient(self.credential)

    def execute_query(self, query: str, timespan=None):
        """
        Executa uma query KQL no Application Insights e retorna os resultados.
        """
        if self.client is None:
            self.authenticate()
        try:
            response = self.client.query_workspace(
                workspace_id=self.workspace_id,
                query=query,
                timespan=timespan
            )
            if response.status == 'Success':
                return response.tables
            else:
                raise Exception(f"Erro ao executar query: {response.status}")
        except HttpResponseError as e:
            raise Exception(f"Erro na consulta ao Azure Application Insights: {str(e)}")
