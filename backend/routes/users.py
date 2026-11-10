from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from pymongo.errors import DuplicateKeyError

from services.user_service import (
    create_user,
    authenticate_user
)

from validators.user_validator import validate_user_data

users_bp = Blueprint("users", __name__)


@users_bp.route("/api/users/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    user_data, error = validate_user_data(data)

    if error:
        return jsonify({"error": error}), 400

    try:
        user = create_user(user_data)

    except DuplicateKeyError:
        return jsonify({
            "error": "Este e-mail já está cadastrado."
        }), 409

    except Exception as error:
        print(f"Erro ao cadastrar usuário: {error}")
        return jsonify({
            "error": "Não foi possível cadastrar o usuário."
        }), 500

    return jsonify({
        "message": "Usuário cadastrado com sucesso.",
        "user": user
    }), 201




@users_bp.route("/api/users/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Envie os dados em formato JSON."
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not isinstance(email, str) or not isinstance(password, str):
        return jsonify({
            "error": "E-mail e senha são obrigatórios."
        }), 400

    user = authenticate_user(email, password)

    if not user:
        return jsonify({
            "error": "E-mail ou senha incorretos."
        }), 401

    access_token = create_access_token(
        identity=user["_id"]
    )

    return jsonify({
        "message": "Login realizado com sucesso.",
        "access_token": access_token,
        "user": user
    }), 200
