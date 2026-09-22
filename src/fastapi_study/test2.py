from uuid import UUID, uuid4
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, Field

app = FastAPI(
    title="ToDo app",
    version="0.0.1"
)

get_router = APIRouter(prefix="/get", tags=["Get Route"])
post_router = APIRouter(prefix="/post", tags=["PostRoute"])
put_router = APIRouter(prefix="/put", tags=["Put Route"])
delete_router = APIRouter(prefix="/delete", tags=["Delete Route"])


class ToDo(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    category: str
    status: bool


class BaseOut(BaseModel):
    msg: str
    error: str


class ToDoCreateOut(BaseOut):
    todo: ToDo


class ToDoGetOut(BaseOut):
    todos: list[ToDo]


db: list[ToDo] = []


@post_router.post("/create")
def create_todo(todo: ToDo):
    db.append(todo)
    return ToDoCreateOut(todo=todo, msg="ToDo Created.")


@get_router.get("/todos")
def fetch_todos():
    return ToDoGetOut(todos=db, msg="ToDos Fetched.")


@get_router.get("/todo/{id}", response_model=ToDoCreateOut | BaseOut)
def fetch_todo(id: str) -> ToDoCreateOut | BaseOut:
    try:
        id = UUID(id)
    except Exception as e:
        return BaseOut(msg="Wrong ID", error=str(e))
    for todo in db:
        if todo.id == id:
            return ToDoCreateOut(todo=todo, msg="ToDo Found.")
    return BaseOut(msg="ToDo Not Found.")


@put_router.put("/todo/{id}", response_model=ToDoCreateOut | BaseModel)
def update_todo(id: str, todo: ToDo) -> ToDoCreateOut | BaseOut:
    try:
        id = UUID(id)
    except Exception as e:
        return BaseOut(msg="Invalid ID", error=str(e))
    for t in db:
        if t.id == id:
            t.name = todo.name
            return ToDoCreateOut(todo=t, msg="Todo Updated.")
    return BaseOut(msg="ToDo with this ID not Found")


@delete_router.delete("/todo/{id}", response_model=BaseOut)
def delete_todo(id: str) -> BaseOut:
    try:
        id = UUID(id)
    except Exception as e:
        return BaseOut(msg="Invalid ID", error=str(e))
    for i, t in db:
        if t.id == id:
            del db[i]
            return BaseOut(msg="Removed ToDo")
    return BaseOut(msg="ToDo not found")


@get_router.get("/category", response_model=ToDoGetOut | BaseOut)
def fetch_todos_by_category(category: str) -> ToDoGetOut | BaseOut:
    todos: list[ToDo] = []
    for todo in db:
        if todo.category == category:
            todos.append(todo)
    if not todos:
        return BaseOut(msg="Todo with given category is not available")
    return ToDoGetOut(todos=todos, msg="Todos Found.")


routers = [get_router, post_router, put_router, delete_router]
for router in routers:
    app.include_router(router=router, prefix="/api")
