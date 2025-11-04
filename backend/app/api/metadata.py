from flask import Blueprint, jsonify
from app.services.azure_insights import AzureInsightsService
import datetime

metadata_bp = Blueprint('metadata', __name__)

# Helper para queries de valores únicos nos últimos 30 dias
def build_distinct_query(field_name):
    return f'''
    traces
    | where timestamp > ago(30d)
    | extend msg_data = parse_json(message)
    | extend val = tostring(msg_data.{field_name})
    | where isnotnull(val) and val != ''
    | summarize count() by val
    | project {field_name}=val
    | order by {field_name} asc
    '''

@metadata_bp.route('/api/metadata/projetos', methods=['GET'])
def get_projetos():
    query = build_distinct_query('projeto')
    try:
        results = AzureInsightsService.run_query(query)
        projetos = [row['projeto'] for row in results if 'projeto' in row]
        return jsonify(projetos), 200
    except Exception as e:
        return jsonify({"error": "Erro ao buscar projetos.", "details": str(e)}), 500

@metadata_bp.route('/api/metadata/usuarios', methods=['GET'])
def get_usuarios():
    query = build_distinct_query('usuario_executor')
    try:
        results = AzureInsightsService.run_query(query)
        usuarios = [row['usuario_executor'] for row in results if 'usuario_executor' in row]
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({"error": "Erro ao buscar usuários.", "details": str(e)}), 500

@metadata_bp.route('/api/metadata/tipos_analise', methods=['GET'])
def get_tipos_analise():
    query = build_distinct_query('tipo_analise')
    try:
        results = AzureInsightsService.run_query(query)
        tipos = [row['tipo_analise'] for row in results if 'tipo_analise' in row]
        return jsonify(tipos), 200
    except Exception as e:
        return jsonify({"error": "Erro ao buscar tipos de análise.", "details": str(e)}), 500

@metadata_bp.route('/api/metadata/modelos', methods=['GET'])
def get_modelos():
    query = build_distinct_query('model_name')
    try:
        results = AzureInsightsService.run_query(query)
        modelos = [row['model_name'] for row in results if 'model_name' in row]
        return jsonify(modelos), 200
    except Exception as e:
        return jsonify({"error": "Erro ao buscar modelos.", "details": str(e)}), 500
