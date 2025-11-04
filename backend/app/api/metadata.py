from flask import Blueprint, jsonify
from datetime import datetime, timedelta
# Supondo que exista um serviço AzureInsightsService já implementado
from app.services.azure_insights import AzureInsightsService

metadata_bp = Blueprint('metadata_bp', __name__)

# Helper para executar queries únicas

def _get_unique_values(column_name: str, days: int = 30):
    since = (datetime.utcnow() - timedelta(days=days)).isoformat() + 'Z'
    kql = f"""
        traces
        | where timestamp > datetime({since})
        | extend msg_data = parse_json(message)
        | extend valor = tostring(msg_data.{column_name})
        | where isnotnull(valor)
        | summarize by valor
        | order by valor asc
    """
    results = AzureInsightsService.run_query(kql)
    return sorted(list(set(row.get('valor') for row in results if row.get('valor') is not None)))

@metadata_bp.route('/api/metadata/projetos', methods=['GET'])
def get_projetos():
    try:
        projetos = _get_unique_values('projeto')
        return jsonify(projetos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@metadata_bp.route('/api/metadata/usuarios', methods=['GET'])
def get_usuarios():
    try:
        usuarios = _get_unique_values('usuario_executor')
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@metadata_bp.route('/api/metadata/tipos_analise', methods=['GET'])
def get_tipos_analise():
    try:
        tipos = _get_unique_values('tipo_analise')
        return jsonify(tipos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@metadata_bp.route('/api/metadata/modelos', methods=['GET'])
def get_modelos():
    try:
        modelos = _get_unique_values('model_name')
        return jsonify(modelos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
