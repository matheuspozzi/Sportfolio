import os

os.environ["MONGO_URI"] = "mongodb://localhost:27017/sportfolio_test"

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from routes.athletes import athletes_bp


@pytest.fixture
def app():
    app = Flask(__name__)

    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "chave-exclusiva-para-testes-somente-local-2026"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    JWTManager(app)

    app.register_blueprint(athletes_bp)

    return app


@pytest.fixture
def client(app):
    return app.test_client()
