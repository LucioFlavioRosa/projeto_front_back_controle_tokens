import os
import requests
import sys

# Script para validar conectividade com Azure Application Insights
# Requer as variáveis: AZURE_APP_INSIGHTS_WORKSPACE_ID, AZURE_APP_INSIGHTS_API_KEY

WORKSPACE_ID = os.getenv("AZURE_APP_INSIGHTS_WORKSPACE_ID")
API_KEY = os.getenv("AZURE_APP_INSIGHTS_API_KEY")

QUERY = "traces | take 1"
API_URL = f"https://api.applicationinsights.io/v1/apps/{WORKSPACE_ID}/query"


def validate_connection():
    if not WORKSPACE_ID or not API_KEY:
        print("[ERRO] Variáveis de ambiente AZURE_APP_INSIGHTS_WORKSPACE_ID ou AZURE_APP_INSIGHTS_API_KEY não definidas.")
        sys.exit(1)

    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    params = {"query": QUERY}

    print(f"[INFO] Testando conexão com workspace_id: {WORKSPACE_ID}")
    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "tables" in data and data["tables"]:
            print("[SUCESSO] Conectividade validada e query executada com sucesso.")
            print(f"[INFO] Linhas retornadas: {data['tables'][0]['rows']}")
        else:
            print("[ERRO] Query executada, mas nenhum dado retornado.")
            sys.exit(2)
    except Exception as e:
        print(f"[ERRO] Falha na conexão ou autenticação: {e}")
        sys.exit(3)

if __name__ == "__main__":
    validate_connection()
