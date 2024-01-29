from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    print("login in successful")
