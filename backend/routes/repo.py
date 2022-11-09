from fastapi import APIRouter
import requests
from backend.database import tokens

router = APIRouter()

@router.get("/github/repos")
async def get_all_repos(user: str):
    access_token = await tokens.get_user_token(user)
    if access_token:
        repos = requests.get("")
