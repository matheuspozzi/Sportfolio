from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from bson import ObjectId

from services.athlete_service import (
    create_athlete,
    list_athletes,
    get_athlete,
    update_athlete,
    delete_athlete
)

from services.athlete_access_service import create_access
from services.authorization_service import check_athlete_permission
from validators.athlete_validator import validate_athlete_data

athletes_bp = Blueprint("athletes", __name__)


@athletes_bp.route("/api/athletes", methods=["POST"])
@jwt_required()
def create():
    user_id = get_jwt_identity()

    data = request.get_json(silent=True)

    athlete_data, error = validate_athlete_data(
        data,
        creating=True
    )

    if error:
        return jsonify({"error": error}), 400

    athlete = create_athlete(athlete_data)

    try:
        create_access(
            user_id=user_id,
            athlete_id=athlete["_id"],
            role="guardian",
            is_primary=True,
            permissions={
                "view": True,
                "edit": True,
                "manage_access": True
            }
        )

    except Exception as error:
        print(f"Erro ao criar acesso do atleta: {error}")

        delete_athlete(athlete["_id"])

        return jsonify({
            "error": "Não foi possível vincular o responsável ao atleta."
        }), 500

    return jsonify({
        "message": "Atleta cadastrado com sucesso.",
        "athlete": athlete
    }), 201

@athletes_bp.route("/api/athletes", methods=["GET"])
@jwt_required()
def list_all():
    user_id = get_jwt_identity()

    athletes = list_athletes(user_id)

    return jsonify({
        "total": len(athletes),
        "athletes": athletes
    }), 200


@athletes_bp.route("/api/athletes/<athlete_id>", methods=["GET"])
@jwt_required()
def get_one(athlete_id):
    if not ObjectId.is_valid(athlete_id):
        return jsonify({"error": "ID de atleta inválido."}), 400

    user_id = get_jwt_identity()

    allowed = check_athlete_permission(
        user_id=user_id,
        athlete_id=athlete_id,
        permission="view"
    )

    if not allowed:
        return jsonify({
            "error": "Você não tem permissão para visualizar este atleta."
        }), 403

    athlete = get_athlete(athlete_id)

    if not athlete:
        return jsonify({"error": "Atleta não encontrado."}), 404

    return jsonify({"athlete": athlete}), 200


@athletes_bp.route("/api/athletes/<athlete_id>", methods=["PATCH"])
@jwt_required()
def update(athlete_id):
    if not ObjectId.is_valid(athlete_id):
        return jsonify({"error": "ID de atleta inválido."}), 400

    user_id = get_jwt_identity()

    allowed = check_athlete_permission(
        user_id=user_id,
        athlete_id=athlete_id,
        permission="edit"
    )

    if not allowed:
        return jsonify({
            "error": "Você não tem permissão para editar este atleta."
        }), 403

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "Envie os dados que deseja atualizar."
        }), 400

    athlete_data, error = validate_athlete_data(data)

    if error:
        return jsonify({"error": error}), 400

    if not athlete_data:
        return jsonify({
            "error": "Nenhum campo permitido foi informado."
        }), 400

    athlete = update_athlete(athlete_id, athlete_data)

    if not athlete:
        return jsonify({"error": "Atleta não encontrado."}), 404

    return jsonify({
        "message": "Atleta atualizado com sucesso.",
        "athlete": athlete
    }), 200

@athletes_bp.route("/api/athletes/<athlete_id>", methods=["DELETE"])
@jwt_required()
def delete(athlete_id):
    if not ObjectId.is_valid(athlete_id):
        return jsonify({
            "error": "ID do atleta inválido."
        }), 400

    user_id = get_jwt_identity()

    allowed = check_athlete_permission(
        user_id=user_id,
        athlete_id=athlete_id,
        permission="manage_access"
    )

    if not allowed:
        return jsonify({
            "error": "Somente o responsável principal pode excluir este atleta."
        }), 403

    deleted = delete_athlete(athlete_id)

    if not deleted:
        return jsonify({
            "error": "Atleta não encontrado."
        }), 404

    return jsonify({
        "message": "Atleta excluído com sucesso."
    }), 200