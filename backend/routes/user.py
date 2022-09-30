from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from backend.database.user import add_user
from backend.models.user import UserSchema

router = APIRouter()


@router.post("/create_user", response_description="User added successfully")
async def create_user(user: UserSchema = Body(...)):
    """
    :param user: request body must contain a JSON object name of the user
    :returns: Returns response "User successfully added"
    """
    user = jsonable_encoder(user)
    await add_user(user)
    return "User successfully added"
