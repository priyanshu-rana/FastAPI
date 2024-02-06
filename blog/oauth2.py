from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from blog import models
from blog.database import get_db

from blog.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token, credentials_exception)


async def get_current_user_id(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        user_token_data = await get_current_user(token)
        user = (
            db.query(models.User)
            .where(models.User.email == user_token_data.email)
            .first()
        )
        return user.id
    except:
        raise credentials_exception
