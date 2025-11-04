from fastapi import APIRouter, Response, status
from azure.identity import ClientSecretCredential
from azure.monitor.query import LogsQueryClient
from app.core.config import settings

router = APIRouter()

@router.get("/api/health", summary="Health check Azure Application Insights")
def health_check():
    try:
        credential = ClientSecretCredential(
            tenant_id=settings.AZURE_TENANT_ID,
            client_id=settings.AZURE_CLIENT_ID,
            client_secret=settings.AZURE_CLIENT_SECRET
        )
        client = LogsQueryClient(credential)
        # Query a simple heartbeat from Application Insights (workspace)
        query = "traces | take 1"
        response = client.query_workspace(
            workspace_id=settings.AZURE_WORKSPACE_ID,
            query=query,
            timespan=None
        )
        if response.tables and len(response.tables[0].rows) >= 0:
            return Response(content="Connected to Azure Application Insights", status_code=status.HTTP_200_OK)
        else:
            return Response(content="No data returned from Azure Application Insights", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response(content=f"Error connecting to Azure Application Insights: {str(e)}", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
