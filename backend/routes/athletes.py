
from flask import Blueprint, request, jsonify
from bson import ObjectId

from services.athlete_service import (
    create_athlete,
    list_athletes,
    get_athlete,
    update_athlete,
    delete_athlete
)

from validators.athlete_validator import validate_athlete_data

athletes_bp = Blueprint("athletes", __name__)


@athletes_bp.route("/api/athletes", methods=["POST"])
def create():
    data = request.get_json(silent=True)

    athlete_data, error = validate_athlete_data(
        data,
        creating=True
    )

    if error:
        return jsonify({"error": error}), 400

    athlete = create_athlete(athlete_data)

    return jsonify({
        "message": "Atleta cadastrado com sucesso.",
        "athlete": athlete
    }), 201


@athletes_bp.route("/api/athletes", methods=["GET"])
def list_all():
    athletes = list_athletes()

    return jsonify({
        "total": len(athletes),
        "athletes": athletes
    }), 200


@athletes_bp.route("/api/athletes/<athlete_id>", methods=["GET"])
def get_one(athlete_id):
    if not ObjectId.is_valid(athlete_id):
        return jsonify({"error": "ID de atleta inválido."}), 400

    athlete = get_athlete(athlete_id)

    if not athlete:
        return jsonify({"error": "Atleta não encontrado."}), 404

    return jsonify({"athlete": athlete}), 200


@athletes_bp.route("/api/athletes/<athlete_id>", methods=["PATCH"])
def update(athlete_id):
    if not ObjectId.is_valid(athlete_id):
        return jsonify({"error": "ID de atleta inválido."}), 400

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
def delete(athlete_id):
    if not ObjectId.is_valid(athlete_id):
        return jsonify({
            "error": "ID do atleta inválido."
        }), 400

    deleted = delete_athlete(athlete_id)

    if not deleted:
        return jsonify({
            "error": "Atleta não encontrado."
        }), 404

    return jsonify({
        "message": "Atleta excluído com sucesso."
    }), 200