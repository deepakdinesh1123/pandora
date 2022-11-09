from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        schema_extra = {"name": "Ashok", "email": "ashok@mail.com"}
