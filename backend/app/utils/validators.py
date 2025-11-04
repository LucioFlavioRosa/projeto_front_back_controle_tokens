import os
from datetime import datetime, timedelta

class ValidationError(Exception):
    pass

def validate_date_range(start: str, end: str, max_days: int = 90):
    """
    Valida que a data final é posterior à inicial e que o range não excede max_days.
    Datas devem estar no formato 'YYYY-MM-DD' ou 'YYYY-MM-DDTHH:MM:SS'.
    """
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    except Exception:
        raise ValidationError("Datas devem estar no formato ISO 8601 (YYYY-MM-DD ou YYYY-MM-DDTHH:MM:SS)")

    if end_dt <= start_dt:
        raise ValidationError("data_fim deve ser posterior a data_inicio.")

    if (end_dt - start_dt).days > max_days:
        raise ValidationError(f"O intervalo de datas não pode exceder {max_days} dias.")

    return True

def validate_azure_credentials():
    """
    Verifica se as principais credenciais do Azure Application Insights estão configuradas via variáveis de ambiente.
    """
    required_vars = [
        "AZURE_APPINSIGHTS_CONNECTION_STRING",
        "AZURE_APPINSIGHTS_APP_ID",
        "AZURE_APPINSIGHTS_API_KEY"
    ]
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        raise ValidationError(f"Variáveis de ambiente Azure faltando: {', '.join(missing)}")
    return True
