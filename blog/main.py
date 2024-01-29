from typing import List
from fastapi import FastAPI
from .database import engine
from . import models
from .routers import blog, user, auth

app = FastAPI()
models.Base.metadata.create_all(engine)


app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)
