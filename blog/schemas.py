from pydantic import BaseModel
from typing import Optional, List


class Blog(BaseModel):
    title: str
    body: str
    is_published: Optional[bool]


class User(BaseModel):
    name: str
    email: str
    password: str


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ShowUserResponseModel(BaseModel):
    id: int
    name: str
    email: str
    blogs: List[Blog]


class ShowBlogResponseModel(BaseModel):
    id: int
    title: str
    body: str
    is_published: Optional[bool]
    creator: ShowUserResponseModel
