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
    # blog.update(request)
    for (
        key,
        value,
    ) in (
        request.dict().items()
    ):  # TODO: Refactor this as dict() method is depricated, also Blog Updation is not working yet
        setattr(blog, key, value)

    db.commit()
    return {"status": "Blog has been updated"}


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()

    return {"status": "Blog has been deleted"}


@app.get("/blogs", status_code=status.HTTP_200_OK)
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blogs not found"
        )
    return blogs


@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
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
