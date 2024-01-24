from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from .database import engine, SessionLocal
from . import schemas, models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .hashing import Hash

app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title, body=request.body, is_published=request.is_published
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    blog.update(dict(request))
    db.commit()
    return {"status": "Blog has been updated", "blog": request}


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    blog.delete(synchronize_session=False)
    db.commit()

    return {"status": "Blog has been deleted"}


@app.get(
    "/blogs",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.ShowBlogResponseModel],
    tags=["Blogs"],
)
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blogs not found"
        )
    return blogs


@app.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlogResponseModel,
    tags=["Blogs"],
)
def get_blog(id, db: Session = Depends(get_db)):
    # blog = db.query(models.Blog).get(id)                              #1
    # blog = db.query(models.Blog).where(models.Blog.id == id).first()  #2
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()  # 3
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    return blog


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/user", response_model=schemas.ShowUserResponseModel, tags=["Users"])
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


@app.get("/users", response_model=List[schemas.ShowUserResponseModel], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )
    return users


@app.get("/user/{id}", response_model=schemas.ShowUserResponseModel, tags=["Users"])
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} is not available",
        )
    return user
