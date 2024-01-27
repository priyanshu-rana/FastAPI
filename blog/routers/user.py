from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import schemas, models
from ..database import get_db
from ..hashing import Hash

router = APIRouter(prefix="/user", tags=["Users"])


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("", response_model=schemas.ShowUserResponseModel)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.becrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/all",
    response_model=List[schemas.ShowUserResponseModel],
)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )
    return users


@router.get(
    "/{id}",
    response_model=schemas.ShowUserResponseModel,
)
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not available",
        )
    return user
