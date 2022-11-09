from pydantic import BaseModel
from fastapi import APIRouter, BackgroundTasks
import requests
from dotenv import load_dotenv
import os

load_dotenv("backend/.env")

class UserAuthModel(BaseModel):
    pass

router = APIRouter()

@router.post("/authenticate/github/")
def get_github_access_token(code: str, background_tasks: BackgroundTasks):
    resp = requests.post("https://github.com/login/oauth/access_token", params={
        "client_id": os.getenv("GITHUB_CLIENT_ID"),
        "client_secret": os.getenv("GITHUB_CLIENT_SECRET"),
        "code": code,
    },
    headers={
        "Accept": "application/json"
    })
    access_token = resp.json()["access_token"]
    background_tasks.add_task(gather_user_details, access_token)
    return {
        "Status": "Success"
    }

def gather_user_details(access_token: str):
