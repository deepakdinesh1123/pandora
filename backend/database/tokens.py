from backend.mongodb import db_client
from backend.database.exceptions import UserAlreadyExists

database = db_client.users
user_token_collection = database.get_collection("users")

async def add_user_token(user_token_data: dict):
    user = await user_token_collection.find_one({"name": user_token_data["name"]})
    if user:
        raise UserAlreadyExists
    insert_token = await user_token_collection.insert_one({"name": user_token_data["name"], "access-token": user_token_data["token"]})

async def get_user_token(user: str):
    access_token = await user_token_collection.find_one({"name": user})
    return access_token
