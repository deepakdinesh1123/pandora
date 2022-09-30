from pydantic import BaseModel, Field

from backend.models.user import UserSchema


class EnvironmentSchema(BaseModel):
    env_name: str = Field(...)
    image_name: str = Field(...)
    system_details: str = Field(...)
    libraries_installed: dict
    environment_variables: dict
    creator: UserSchema = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "env_name": "ubuntu-django",
                "image_name": "ubuntu",
                "system_details": "Ubuntu 22.04",
                "libraries_installed": ["django", "gunicorn", "python"],
                "environment_variables": {},
                "creator_id": "125648162543ftasf",
            }
        }
