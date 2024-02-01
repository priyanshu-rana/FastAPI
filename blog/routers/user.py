from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services.user_service import UserService
from blog.oauth2 import get_current_user

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("", response_model=schemas.ShowUserResponseModel)
def create_user(
    request: schemas.User,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return UserService.create_user(request, db)


@router.get(
    "/all",
    response_model=List[schemas.ShowUserResponseModel],
)
def get_users(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return UserService.get_users(db)


@router.get(
    "/{id}",
    response_model=schemas.ShowUserResponseModel,
)
def get_user(
    id,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return UserService.get_user(id, db)
