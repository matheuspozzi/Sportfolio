from datetime import datetime, timezone

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database import db

collection = db["users"]
collection.create_index("email", unique=True)

def create_user(data):
    now = datetime.now(timezone.utc)

    user = {
        "name": data["name"],
        "email": data["email"],
        "password_hash": generate_password_hash(data["password"]),
        "email_verified": False,
        "created_at": now,
        "updated_at": now
    }

    result = collection.insert_one(user)

    return {
        "_id": str(result.inserted_id),
        "name": user["name"],
        "email": user["email"],
        "email_verified": user["email_verified"],
        "created_at": user["created_at"]
    }

def authenticate_user(email, password):
    user = collection.find_one({
        "email": email.strip().lower()
    })

    if not user:
        return None

    password_valid = check_password_hash(
        user["password_hash"],
        password
    )

    if not password_valid:
        return None

    return {
        "_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "email_verified": user["email_verified"]
    }