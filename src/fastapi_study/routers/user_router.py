from fastapi import APIRouter

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/signin")
def signin() -> dict:
    return {"msg": "User Sign In"}


@user_router.get("signup")
def signup() -> dict:
    return {"msg": "User Sign Up"}
