from fastapi import FastAPI

from fastapi_study.routers import todo_router, user_router

app = FastAPI(
    title="Todo App",
    version="0.0.2"
)

app.include_router(router=todo_router, prefix="/api")
app.include_router(router=user_router, prefix="/api")
