from pydantic import BaseModel, Field, HttpUrl


class Repository(BaseModel):
    name: str = Field(...)
    repo_url: HttpUrl = Field(...)
