import os
from flask import Flask, jsonify
from flask_cors import CORS

# Import blueprints (devem ser implementados em arquivos separados)
try:
    from .routes.analytics import analytics_bp
except ImportError:
    analytics_bp = None
try:
    from .routes.metadata import metadata_bp
except ImportError:
    metadata_bp = None

def create_app():
    """
    Factory function para criar e configurar a aplicação Flask.
    - Configura CORS para permitir origens do frontend.
    - Registra blueprints de analytics e metadata.
    - Adiciona handlers globais de erro.
    - Adiciona endpoint de health check.
    """
    app = Flask(__name__)

    # Configuração CORS
    frontend_origin = os.environ.get("FRONTEND_ORIGIN", "*")
    CORS(app, resources={r"/api/*": {"origins": frontend_origin}}, supports_credentials=True)

    # Registro dos blueprints (se existirem)
    if analytics_bp:
        app.register_blueprint(analytics_bp, url_prefix="/api/analytics")
    if metadata_bp:
        app.register_blueprint(metadata_bp, url_prefix="/api/metadata")

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    # Handlers globais de erro
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500

    return app
