from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel
from typing import Annotated
from tinydb import TinyDB, Query as TinyQuery, where

tiny = TinyDB("db.json")

usersDB = tiny.table("users")

bannedDB = tiny.table("ban")


class User(BaseModel):
    name: str
    device_name: str
    product: str
    id: str


app = FastAPI()

allow_new_users: bool = True



def check_existence(user: User):
    query = TinyQuery()
    return (
        (query.name == user.name) &
        (query.device_name == user.device_name) &
        (query.product == user.product) &
        (query.id == user.id)
    )


@app.get(
    "/get-user",
    responses={
        200: {"content": {"application/json": {"example": "Allowed"}}},
        400: {"content": {"application/json": {"example": {"detail": "msg"}}}},
    },
    tags=["Auth"],
)
def get_user(user: Annotated[User, Query()]) -> str:
    print(check_existence(user))
    ban = bannedDB.search(check_existence(user))
    if ban:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Exists but Banned")
    auth = usersDB.contains(check_existence(user))
    if auth:
        return "Allowed"
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Does not exist")


@app.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"content": {"application/json": {"example": "Success"}}},
        401: {"content": {"application/json": {"example": {"detail": "msg"}}}},
    },
    tags=["Auth"],
)
def create_user(user: User):
    if allow_new_users:
        usersDB.insert(user.model_dump())
        return "Success"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not allowing creation of new users",
        )


@app.get(
    "/get-all-users",
    tags=["Auth"],
)
def get_all_users() -> list[User]:
    # Remember to add security for this
    return usersDB.all()


@app.post(
    "/ban",
    responses={
        200: {"content": {"application/json": {"example": "Banned user"}}},
        401: {"content": {"application/json": {"example": {"detail": "msg"}}}},
    },
    tags=["Ban"],
)
def ban(user: str):
    userDB = usersDB.get(where("name") == user)
    if userDB:
        if not bannedDB.contains(TinyQuery().name == userDB.get("name")):
            bannedDB.insert(userDB.copy())
        return f"Banned {user}"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )


@app.post(
    "/unban",
    responses={
        200: {"content": {"application/json": {"example": "UnBanned user"}}},
        401: {"content": {"application/json": {"example": {"detail": "msg"}}}},
    },
    tags=["Ban"],
)
def unban(user: str):
    bans = bannedDB.remove(where("name") == user)
    if bans:
        return f"UnBanned {user}"
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )


@app.get(
    "/ban-list",
    tags=["Ban"],
)
def get_ban_list() -> list[User]:
    # Remember to add some security
    return bannedDB.all()


@app.post("/ban-all", tags=["Ban"])
def ban_all():
    users = [User(**user) for user in usersDB.all()]
    for user in users:
        ban(user.name)
    return "Banned All"


@app.post("/unban-all", tags=["Ban"])
def unban_all():
    users: list[User] = [User(**user) for user in bannedDB.all()]
    for user in users:
        unban(user.name)
    return "Unbanned All"
