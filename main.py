from fastapi import FastAPI
from typing import Optional
from blog.schemas import Blog


app = FastAPI()


@app.get("/blogs")
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    #  fetch blogs
    if published:
        return {"data": f"{limit} published blogs", "sort_type": sort}
    else:
        return {"data": f"{limit} blogs", "sort_type": sort}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{id}")
def blog(id: int):
    #  fetch blog with id=id
    return {"data": id}


@app.get("/blog/{id}/comments")
def comments(id: int):
    #  fetch comments of blog with id=id
    return {"data": {"1", "2"}}


@app.post("/blog")
def create_blog(request: Blog):
    return {
        "data": f"Blog is created with titile '{request.title}', with body '{request.body}'"
    }


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9999)
