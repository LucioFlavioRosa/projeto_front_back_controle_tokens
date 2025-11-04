import os
from datetime import datetime, timedelta

class ValidationError(Exception):
    pass

def validate_date_range(start, end, max_days=90):
    """
    Valida que end > start e que o range não excede max_days (padrão: 90).
    Parâmetros:
        start (str): data inicial no formato 'YYYY-MM-DD'
        end (str): data final no formato 'YYYY-MM-DD'
        max_days (int): número máximo de dias permitidos
    Lança ValidationError em caso de erro.
    """
    try:
        dt_start = datetime.strptime(start, '%Y-%m-%d')
        dt_end = datetime.strptime(end, '%Y-%m-%d')
    except Exception:
        raise ValidationError('Datas devem estar no formato YYYY-MM-DD.')
    if dt_end <= dt_start:
        raise ValidationError('A data final deve ser posterior à data inicial.')
    if (dt_end - dt_start).days > max_days:
        raise ValidationError(f'O intervalo de datas não pode exceder {max_days} dias.')
    return True

def validate_azure_credentials():
    """
    Verifica se as principais credenciais do Azure Application Insights estão configuradas via variáveis de ambiente.
    Lança ValidationError se faltar alguma.
    """
    required_vars = ['AZURE_APPINSIGHTS_CONNECTION_STRING', 'AZURE_APPINSIGHTS_APP_ID', 'AZURE_APPINSIGHTS_API_KEY']
    missing = [var for var in required_vars if not os.environ.get(var)]
    if missing:
        raise ValidationError(f'Credenciais Azure faltando: {", ".join(missing)}')
    return True
