from backend.mongodb import db_client

database = db_client.users
user_token_collection = database.get_collection("tokens")


def add_user_token(user_token_data: dict):
    user = user_token_collection.find_one({"username": user_token_data["username"]})
    if user:
        user_token_collection.update_one(
            {"username": user_token_data["username"]},
            {"$set": {"access-token": user_token_data["access-token"]}},
        )
    else:
        user_token_collection.insert_one(
            {
                "username": user_token_data["username"],
                "access-token": user_token_data["access-token"],
            }
        )


def get_user_token(user: str):
    access_token = user_token_collection.find_one({"username": user})
    return access_token
