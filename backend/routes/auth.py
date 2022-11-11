import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, BackgroundTasks

from backend.database import repository, tokens, user

load_dotenv("backend/.env")


router = APIRouter()


@router.post("/authenticate/github/")
def get_github_access_token(code: str, background_tasks: BackgroundTasks):
    resp = requests.post(
        "https://github.com/login/oauth/access_token",
        params={
            "client_id": os.getenv("GITHUB_CLIENT_ID"),
            "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
            "code": code,
        },
        headers={"Accept": "application/json"},
    )
    access_token = resp.json()["access_token"]
    background_tasks.add_task(gather_user_details, access_token)
    return {"Status": "Success"}


def gather_user_details(access_token: str):
    # Username, email
    resp = requests.get(
        "https://api.github.com/user",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        },
    )
    user_data = resp.json()
    username = user_data["login"]
    email = user_data["email"]
    req_user_data = {"username": username, "email": email}
    try:
        user.add_user(req_user_data)
    except Exception:
        pass

    # Insert access token
    user_token_data = {"username": username, "access-token": access_token}
    try:
        tokens.add_user_token(user_token_data)
    except Exception:
        pass

    # Repo Info
    resp = requests.get(
        "https://api.github.com/user/repos",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github+json",
        },
    )
    repositories = resp.json()
    if isinstance(repositories, dict) and repositories.get("message"):
        print("Failure")
    else:
        repository.add_repositories(repositories, username)
