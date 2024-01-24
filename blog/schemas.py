from pydantic import BaseModel
from typing import Optional


class Blog(BaseModel):
    title: str
    body: str
    is_published: Optional[bool]


class ShowBlogResponseModel(BaseModel):
    id: int
    title: str
    body: str
    is_published: Optional[bool]

    class Config:
        from_attributes = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUserResponseModel(BaseModel):
    id: int
    name: str
    email: str
