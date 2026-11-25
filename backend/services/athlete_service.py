from services.athlete_access_service import collection as access_collection
from datetime import datetime, timezone
from bson import ObjectId

from database import db

collection = db["athletes"]


def serialize_athlete(athlete):
    if not athlete:
        return None

    athlete = athlete.copy()
    athlete["_id"] = str(athlete["_id"])

    return athlete


def create_athlete(data):
    now = datetime.now(timezone.utc)

    athlete = {
        **data,
        "profile_photo_url": None,
        "privacy": {
            "profile_public": False
        },
        "created_at": now,
        "updated_at": now
    }

    result = collection.insert_one(athlete)

    athlete["_id"] = str(result.inserted_id)

    return athlete


def list_athletes(user_id):
    accesses = access_collection.find({
        "user_id": ObjectId(user_id),
        "status": "active"
    })

    athlete_ids = [
        access["athlete_id"]
        for access in accesses
    ]

    athletes = list(
        collection.find({
            "_id": {"$in": athlete_ids}
        }).sort("created_at", -1).limit(100)
    )

    return [serialize_athlete(a) for a in athletes]


def get_athlete(athlete_id):
    athlete = collection.find_one({
        "_id": ObjectId(athlete_id)
    })

    if not athlete:
        return None

    return serialize_athlete(athlete)


def update_athlete(athlete_id, data):
    update_data = {
        **data,
        "updated_at": datetime.now(timezone.utc)
    }

    result = collection.update_one(
        {"_id": ObjectId(athlete_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return None

    return get_athlete(athlete_id)

def delete_athlete(athlete_id):
    athlete_object_id = ObjectId(athlete_id)

    result = collection.delete_one({
        "_id": athlete_object_id
    })

    if result.deleted_count == 0:
        return False

    access_collection.delete_many({
        "athlete_id": athlete_object_id
    })

    return True