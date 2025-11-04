class AzureInsightsException(Exception):
    """Exceção base para erros relacionados ao Azure Application Insights."""
    def __init__(self, message: str = "Erro no Azure Application Insights"):
        super().__init__(message)

class QueryExecutionException(AzureInsightsException):
    """Exceção para erros na execução de queries KQL."""
    def __init__(self, message: str = "Erro ao executar a query KQL"):
        super().__init__(message)

class InvalidParametersException(AzureInsightsException):
    """Exceção para parâmetros inválidos fornecidos à API ou query builder."""
    def __init__(self, message: str = "Parâmetros inválidos fornecidos"):
        super().__init__(message)
