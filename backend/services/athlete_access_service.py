from datetime import datetime, timezone

from bson import ObjectId
from pymongo import ASCENDING

from database import db

collection = db["athlete_access"]


# Índices para evitar vínculos duplicados e mais de um titular principal.
def initialize_indexes():
    collection.create_index(
        [("user_id", ASCENDING), ("athlete_id", ASCENDING)],
        unique=True,
        partialFilterExpression={"status": "active"}
    )

    collection.create_index(
        [("athlete_id", ASCENDING)],
        unique=True,
        partialFilterExpression={
            "status": "active",
            "is_primary": True
        }
    )


VALID_ROLES = {"guardian", "athlete", "editor", "viewer"}

VALID_PERMISSIONS = {
    "view",
    "edit",
    "manage_access"
}


def serialize_access(access):
    if not access:
        return None

    access = access.copy()

    access["_id"] = str(access["_id"])
    access["user_id"] = str(access["user_id"])
    access["athlete_id"] = str(access["athlete_id"])

    if access.get("granted_by"):
        access["granted_by"] = str(access["granted_by"])

    return access


def create_access(
    user_id,
    athlete_id,
    role,
    is_primary=False,
    permissions=None,
    granted_by=None
):
    if role not in VALID_ROLES:
        raise ValueError("Tipo de acesso inválido.")


    if permissions is not None:
        if not isinstance(permissions, dict):
            raise ValueError("Permissões devem ser um dicionário.")

        if not set(permissions).issubset(VALID_PERMISSIONS):
            raise ValueError("Permissão inválida.")

        if not all(type(value) is bool for value in permissions.values()):
            raise ValueError("Valor de permissão inválido.")

    now = datetime.now(timezone.utc)

    access = {
        "user_id": ObjectId(user_id),
        "athlete_id": ObjectId(athlete_id),
        "role": role,
        "status": "active",
        "is_primary": is_primary,
        "permissions": permissions if permissions is not None else {
            "view": True,
            "edit": False,
            "manage_access": False
        },
        "granted_by": ObjectId(granted_by) if granted_by else None,
        "created_at": now,
        "updated_at": now
    }

    result = collection.insert_one(access)

    access["_id"] = result.inserted_id

    return serialize_access(access)


def get_user_access_for_athlete(user_id, athlete_id):
    access = collection.find_one({
        "user_id": ObjectId(user_id),
        "athlete_id": ObjectId(athlete_id),
        "status": "active"
    })

    return serialize_access(access)


def list_athlete_access(athlete_id):
    accesses = collection.find({
        "athlete_id": ObjectId(athlete_id),
        "status": "active"
    }).sort("created_at", ASCENDING)

    return [serialize_access(access) for access in accesses]


def has_permission(user_id, athlete_id, permission):
    if not ObjectId.is_valid(user_id):
        return False

    if not ObjectId.is_valid(athlete_id):
        return False

    if permission not in VALID_PERMISSIONS:
        return False

    access = collection.find_one({
        "user_id": ObjectId(user_id),
        "athlete_id": ObjectId(athlete_id),
        "status": "active"
    })

    if not access:
        return False

    if access.get("is_primary"):
        return True

    permissions = access.get("permissions")

    if not isinstance(permissions, dict):
        return False

    return permissions.get(permission, False) is True

def is_primary_responsible(user_id, athlete_id):
    if not ObjectId.is_valid(user_id):
        return False

    if not ObjectId.is_valid(athlete_id):
        return False

    access = collection.find_one({
        "user_id": ObjectId(user_id),
        "athlete_id": ObjectId(athlete_id),
        "status": "active",
        "is_primary": True
    })

    return access is not None
