from flask import Blueprint, request, jsonify
from app.services.data_processor import DataProcessor
from app.services.azure_insights import AzureInsightsService
from app.services.query_builder import QueryBuilder
from app.schemas.query_params import QueryParams
from marshmallow import ValidationError
import logging

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics/tokens', methods=['POST'])
def analytics_tokens():
    try:
        # Validação do payload
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Payload JSON ausente."}), 400
        try:
            params = QueryParams().load(json_data)
        except ValidationError as ve:
            return jsonify({"error": "Payload inválido.", "details": ve.messages}), 400

        # Monta a query KQL
        kql_query = QueryBuilder.build_tokens_query(params)
        if not kql_query:
            return jsonify({"error": "Não foi possível construir a query para os parâmetros fornecidos."}), 400

        # Executa a query no Azure Application Insights
        try:
            results = AzureInsightsService.run_query(kql_query)
        except AzureInsightsService.UnauthorizedException:
            return jsonify({"error": "Não autorizado a acessar o Application Insights."}), 401
        except Exception as e:
            logging.exception("Erro ao consultar Application Insights")
            return jsonify({"error": "Erro ao consultar Application Insights.", "details": str(e)}), 500

        # Processa os resultados para o frontend
        output = DataProcessor.process_query_results(results, params)
        return jsonify(output), 200

    except Exception as e:
        logging.exception("Erro inesperado no endpoint de analytics tokens")
        return jsonify({"error": "Erro interno do servidor.", "details": str(e)}), 500
