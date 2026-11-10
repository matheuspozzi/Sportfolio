
from flask import Flask, jsonify

from database import test_connection
from routes.athletes import athletes_bp

app = Flask(__name__)

app.register_blueprint(athletes_bp)


@app.route("/api/health", methods=["GET"])
def health():
    try:
        test_connection()

        return jsonify({
            "status": "online",
            "database": "connected",
            "application": "Sportfolio"
        }), 200

    except Exception as error:
        print(f"Erro de conexão: {error}")

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
