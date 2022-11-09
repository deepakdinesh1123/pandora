from bson.objectid import ObjectId

from backend.database.exceptions import UserAlreadyExists
from backend.mongodb import db_client

database = db_client.users
user_collection = database.get_collection("users")


def user_helper(user) -> dict:
    return {"id": str(user["_id"]), "name": user["name"]}


async def get_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


async def get_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


async def add_user(user_data: dict):
    user = user_collection.find_one({"name": user_data["name"]})
    if user:
        raise UserAlreadyExists
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)
