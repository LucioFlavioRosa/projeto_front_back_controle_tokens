import os
from app import create_app

if __name__ == "__main__":
    app = create_app()
    env = os.environ.get("FLASK_ENV", "production")
    debug = env == "development"
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug)
