import os
from services.user_service import initialize_user_indexes
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from database import test_connection
from routes.athletes import athletes_bp
from routes.users import users_bp
from services.athlete_access_service import initialize_indexes
from pymongo.errors import PyMongoError


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

if not app.config["JWT_SECRET_KEY"]:
    raise RuntimeError("JWT_SECRET_KEY não foi configurada.")

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

jwt = JWTManager(app)

app.register_blueprint(athletes_bp)
app.register_blueprint(users_bp)

initialize_indexes()
initialize_user_indexes()


@app.route("/api/health", methods=["GET"])
def health():
    try:
        test_connection()

        return jsonify({
            "status": "online",
            "database": "connected",
            "application": "Sportfolio"
        }), 200

    except PyMongoError:
        app.logger.exception("Erro de conexão com o MongoDB.")

        return jsonify({
            "status": "error",
            "database": "disconnected"
        }), 500
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )
