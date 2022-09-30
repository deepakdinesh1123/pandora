from pydantic import BaseModel, Field

from backend.models.user import UserSchema


class ImageSchema(BaseModel):
    image_name: str = Field(...)
    image_owner: UserSchema = Field(...)
    tags = list[str] = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "image_name": "ubuntu",
                "image_owner": "Ashok",
                "tags": ["latest", "1.0", "2.0"],
            }
        }
