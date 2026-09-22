from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI(
    title="test fastapi app",
    description="This is just for learning",
    version="0.0.1"
)


@app.get("/")
def hello():
    return {"message": "Hello check"}


@app.get("/list", include_in_schema=False)
def list_of_values():
    return [1, 2, 3]


@app.post("/create")
def create_something(data: dict):
    return {"data": data, "msg": "created successfully"}


@app.put("/update/{id}")
def update_something(id: str, data: dict):
    return {"id": id, "data": data, "msg": "updated"}


@app.delete("/delete/{id}", tags=["delete"])
def delete_something(id: str):
    return {"id": id, "msg": "deleted successfully"}


class Post(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(extra="forbid")


class PostOut(BaseModel):
    post: Post
    msg: str


@app.post("/create_post", response_model=PostOut, summary="", description="",
          tags=["Post"], status_code=201)
def create_post(post: Post) -> PostOut:
    return {"post": post, "msg": "created post"}
