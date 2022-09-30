from backend.mongodb import db_client

database = db_client.images


def image_helper(image):
    return {
        "id": image["_id"],
        "image_name": image["image_name"],
        "image_owner_id": image["image_owner_id"],
        "tags": image["tags"],
    }
