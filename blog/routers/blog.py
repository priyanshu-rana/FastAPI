from fastapi import APIRouter
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services.blog_service import BlogService
from blog.oauth2 import get_current_user

router = APIRouter(prefix="/blog", tags=["Blogs"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    return BlogService.create(request, db)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    return BlogService.update(id, request, db)


@router.delete("/{id}", status_code=status.HTTP_200_OK)  # can be use 204
def delete(id, db: Session = Depends(get_db)):
    return BlogService.delete(id, db)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowBlogResponseModel],
)
def get_blogs(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return BlogService.get_all(db)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlogResponseModel,
)
def get_blog(id, db: Session = Depends(get_db)):
    return BlogService.get_blog(id, db)
