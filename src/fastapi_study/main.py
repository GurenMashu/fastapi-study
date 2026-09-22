import json
from time import perf_counter
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from fastapi_study.routers import todo_router, user_router

app = FastAPI(
    title="Todo App",
    version="0.0.2"
)

limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exec: JSONResponse(
        status_code=429,
        content={
            "detail": "Too manu request"
        }
    )
)

app.add_middleware(SlowAPIMiddleware)

app.state.request_count = 0


@app.middleware("http")
async def request_details(request: Request, call_next):
    print(request["path"])
    print(request["method"])
    payload = await request.body
    if payload:
        print(json.loads(payload))
    start = perf_counter()
    app.state.request_count += 1
    # print(app.state.request_count)
    response = await call_next(request)
    end = perf_counter()
    print(end - start)
    return response


app.include_router(router=todo_router, prefix="/api")
app.include_router(router=user_router, prefix="/api")
