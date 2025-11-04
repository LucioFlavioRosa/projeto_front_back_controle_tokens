import os
from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    # Configurações de CORS - permitir origens do frontend (ajustar conforme necessário)
    frontend_origin = os.environ.get('FRONTEND_ORIGIN', '*')
    CORS(app, resources={r"/*": {"origins": frontend_origin}})

    # Registro dos blueprints (devem ser implementados em app/analytics.py e app/metadata.py)
    try:
        from .analytics import analytics_bp
        app.register_blueprint(analytics_bp, url_prefix='/analytics')
    except ImportError:
        pass  # Blueprint ainda não implementado
    try:
        from .metadata import metadata_bp
        app.register_blueprint(metadata_bp, url_prefix='/metadata')
    except ImportError:
        pass  # Blueprint ainda não implementado

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "ok"}), 200

    # Error handlers globais
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
