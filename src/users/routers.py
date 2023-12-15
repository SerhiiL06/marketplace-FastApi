from fastapi import APIRouter, Depends
from .schemes import RegisterUser, LoginUser, Token
from .models import User
from .crud import UserCRUD
from .authentication import UserAuth, current_user
from typing import Annotated
from database.depends import db_depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/register")
async def register(data: RegisterUser, db: db_depends):
    crud = UserCRUD()
    crud.create_user(data, db)

    return {"message": "register success"}


@users_router.post("/token", response_model=Token)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_depends):
    auth = UserAuth()

    token = auth.login(data, db)

    return {"access_token": token, "token_type": "bearer"}


@users_router.get("/user-list")
async def user_list(db: db_depends, user: current_user):
    pass
