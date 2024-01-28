from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services.user_service import UserService

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("", response_model=schemas.ShowUserResponseModel)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return UserService.create_user(request, db)


@router.get(
    "/all",
    response_model=List[schemas.ShowUserResponseModel],
)
def get_users(db: Session = Depends(get_db)):
    return UserService.get_users(db)


@router.get(
    "/{id}",
    response_model=schemas.ShowUserResponseModel,
)
def get_user(id, db: Session = Depends(get_db)):
    return UserService.get_user(id, db)
