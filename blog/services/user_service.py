from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from blog import models, schemas
from blog.database import SessionLocal, get_db
from ..hashing import Hash


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def create_user(request: schemas.User, db: SessionLocal = Depends(get_db)):
        new_user = models.User(
            name=request.name,
            email=request.email,
            password=Hash.becrypt(request.password),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_users(db: Session = Depends(get_db)):
        users = db.query(models.User).all()
        if not users:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
            )
        return users

    def get_user(id, db: Session = Depends(get_db)):
        user = db.query(models.User).get(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {id} is not available",
            )
        return user
