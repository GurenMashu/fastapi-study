from uuid import UUID, uuid4
from fastapi import APIRouter, Response, Request
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address


todo_router = APIRouter(prefix="/todo", tags=["ToDo"])

limiter = Limiter(key_func=get_remote_address)


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
    api_count: int


class ToDoGetOut(BaseOut):
    todos: list[ToDo]


db: list[ToDo] = []


@todo_router.post("/create", response_model=ToDoCreateOut)
@limiter.limit("2/minute")
def create_todo(request: Request, todo: ToDo) -> ToDoCreateOut:
    db.append(todo)
    return ToDoCreateOut(
        todo=todo,
        msg="ToDo Created.",
        api_count=request.app.state.request_count)


@todo_router.get("/todos", response_model=ToDoGetOut)
@limiter.limit("3/minute")
def fetch_todos() -> ToDoGetOut:
    return ToDoGetOut(todos=db, msg="ToDos Fetched.")


@todo_router.get("/todo/{id}", response_model=ToDoCreateOut | BaseOut)
def fetch_todo(id: str) -> ToDoCreateOut | BaseOut:
    try:
        id = UUID(id)
    except Exception as e:
        return Response(content=BaseOut(
                            msg="Wrong ID", error=str(e)).model_dump_json(),
                        status_code=400)
    for todo in db:
        if todo.id == id:
            return Response(
                content=ToDoCreateOut(
                    todo=todo,
                    msg="ToDo Found.").model_dump_json(),
                status_code=200)
    return Response(
        content=BaseOut(msg="ToDo Not Found."),
        status_code=404)


@todo_router.put("/todo/{id}", response_model=ToDoCreateOut | BaseModel)
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


@todo_router.delete("/todo/{id}", response_model=BaseOut)
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


@todo_router.get("/category", response_model=ToDoGetOut | BaseOut)
def fetch_todos_by_category(category: str) -> ToDoGetOut | BaseOut:
    todos: list[ToDo] = []
    for todo in db:
        if todo.category == category:
            todos.append(todo)
    if not todos:
        return BaseOut(msg="Todo with given category is not available")
    return ToDoGetOut(todos=todos, msg="Todos Found.")
