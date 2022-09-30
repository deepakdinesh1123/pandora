from backend.mongodb import db_client

database = db_client.environments


def environment_helper(environment) -> dict:
    return {
        "id": str(environment["_id"]),
        "env_name": environment["env_name"],
        "image_name": environment["image_name"],
        "system_details": environment["system_details"],
        "libraries_installed": environment["libraries_installed"],
        "environment_variables": environment["environment_variables"],
        "creator_id": environment["creator_id"],
    }
