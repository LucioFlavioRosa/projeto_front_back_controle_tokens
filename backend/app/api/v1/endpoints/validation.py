from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Optional
import os
import requests

router = APIRouter()

class ValidationResponse(BaseModel):
    success: bool
    message: str
    details: Optional[dict] = None

@router.post("/validate-connection", response_model=ValidationResponse, status_code=status.HTTP_200_OK)
def validate_connection():
    """
    Testa a conexão com o Azure Application Insights usando a connection string definida na variável de ambiente.
    """
    connection_string = os.getenv("APPINSIGHTS_CONNECTION_STRING")
    if not connection_string:
        return ValidationResponse(success=False, message="Variável de ambiente APPINSIGHTS_CONNECTION_STRING não encontrada.")

    # Extrai o InstrumentationKey da connection string
    try:
        parts = dict(item.split('=', 1) for item in connection_string.split(';') if '=' in item)
        instrumentation_key = parts.get('InstrumentationKey')
        if not instrumentation_key:
            return ValidationResponse(success=False, message="InstrumentationKey não encontrado na connection string.")
    except Exception as e:
        return ValidationResponse(success=False, message=f"Erro ao processar a connection string: {str(e)}")

    # Endpoint de teste: consulta simples de métricas (API REST do Application Insights)
    # Documentação: https://dev.applicationinsights.io/documentation/Using-the-API/Query
    api_url = f"https://api.applicationinsights.io/v1/apps/{instrumentation_key}/metrics/requests/count"
    headers = {
        "x-api-key": instrumentation_key
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        if response.status_code == 200:
            return ValidationResponse(success=True, message="Conexão com o Azure Application Insights bem-sucedida.")
        else:
            return ValidationResponse(success=False, message=f"Falha ao conectar: {response.status_code} - {response.text}")
    except Exception as e:
        return ValidationResponse(success=False, message=f"Erro ao conectar: {str(e)}")
