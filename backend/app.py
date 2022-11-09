from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes import build, container, execute, user, auth

origins = ["http://localhost:3000"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(build.router)
app.include_router(container.router)
app.include_router(execute.router)
app.include_router(user.router)
app.include_router(auth.router)
