from backend.database import exceptions
from backend.mongodb import db_client

database = db_client.repositories
repo_collection = database.get_collection("repo_data")


def add_repositories(repo_data: list, username: str):
    user_repo_data = {"username": username, "repositories": []}
    for repo in repo_data:
        req_data = {"repo_name": repo["name"], "url": repo["clone_url"]}
        user_repo_data["repositories"].append(req_data)

    user = repo_collection.find_one({"username": username})
    if user:
        repo_collection.update_one(
            {"username": username},
            {"$set": {"repositories": user_repo_data["repositories"]}},
        )
    else:
        user = repo_collection.insert_one(user_repo_data)


def get_all_repositories(username: str):
    user = repo_collection.find_one({"username": username})
    if not username:
        raise exceptions.UserDoesNotExist
    else:
        return user["repositories"]
