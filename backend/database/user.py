from bson.objectid import ObjectId

from backend.database.exceptions import UserAlreadyExists
from backend.mongodb import db_client

database = db_client.users
user_collection = database.get_collection("user_data")


def user_helper(user) -> dict:
    return {"id": str(user["_id"]), "username": user["username"]}


async def get_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


def get_user(id: str):
    user = user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


def add_user(user_data: dict):
    user = user_collection.find_one({"username": user_data["username"]})
    if user:
        raise UserAlreadyExists
    user = user_collection.insert_one(user_data)
    new_user = user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)
