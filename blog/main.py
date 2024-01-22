from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from .database import engine, SessionLocal
from . import schemas, models
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title, body=request.body, is_published=request.is_published
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    blog.update(dict(request))
    db.commit()
    return {"status": "Blog has been updated", "blog": request}


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.post("/user")
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=request.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
