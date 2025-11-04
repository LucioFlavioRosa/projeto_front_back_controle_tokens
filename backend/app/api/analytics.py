from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError
from app.services.data_processor import DataProcessor
# Supondo que existam os módulos abaixo:
from app.services.query_builder import QueryBuilder
from app.services.azure_insights import AzureInsightsService
from app.schemas.query_params import QueryParams

analytics_bp = Blueprint('analytics_bp', __name__)

@analytics_bp.route('/api/analytics/tokens', methods=['POST'])
def analytics_tokens():
    try:
        payload = request.get_json()
        if not payload:
            raise BadRequest("Payload JSON ausente ou inválido.")

        # Validação do payload usando QueryParams
        try:
            params = QueryParams(**payload)
        except Exception as e:
            raise BadRequest(f"Erro de validação dos parâmetros: {str(e)}")

        # Gera a query KQL
        try:
            kql_query = QueryBuilder.build_tokens_query(params)
        except Exception as e:
            raise BadRequest(f"Erro ao gerar a query: {str(e)}")

        # Executa a query via AzureInsightsService
        try:
            results = AzureInsightsService.run_query(kql_query)
        except Unauthorized as e:
            return jsonify({"error": "Não autorizado", "details": str(e)}), 401
        except Exception as e:
            raise InternalServerError(f"Erro ao executar a query no Azure: {str(e)}")

        # Processa resultados com DataProcessor
        try:
            data = DataProcessor.process_query_results(results, params)
        except Exception as e:
            raise InternalServerError(f"Erro ao processar os resultados: {str(e)}")

        return jsonify(data), 200

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Unauthorized as e:
        return jsonify({"error": str(e)}), 401
    except InternalServerError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Erro inesperado.", "details": str(e)}), 500
