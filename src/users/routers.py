from fastapi import APIRouter, Depends, HTTPException, status
from .schemes import (
    RegisterUser,
    UserRead,
    Token,
    ChangePassword,
    DefaultUserUpdate,
    Role,
)

from .crud import UserCRUD
from .authentication import UserAuth, current_user
from typing import Annotated
from database.depends import db_depends
from fastapi.security import OAuth2PasswordRequestForm


users_router = APIRouter(prefix="/users", tags=["users"])

crud = UserCRUD()


@users_router.post("/register")
async def register(data: RegisterUser, db: db_depends):
    crud.create_user(data, db)

    return {"message": "register success"}


@users_router.post("/token", response_model=Token)
async def login(data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_depends):
    auth = UserAuth()

    token = auth.login(data, db)

    return {"access_token": token, "token_type": "bearer"}


@users_router.post("/change-password")
async def change_password(
    password_data: ChangePassword,
    user: current_user,
    db: db_depends,
):
    crud = UserCRUD()

    crud.change_password(token_data=user, password=password_data, db=db)

    return {"message": "password was edit"}


@users_router.get(
    "/me",
    response_model=UserRead,
    response_model_exclude=["id", "is_active", "role", "join_at"],
)
async def my_profile(user: current_user, db: db_depends):
    data = crud.retrieve_user(user.get("user_id"), db)

    return data


@users_router.patch("/me")
async def update_user(
    data: DefaultUserUpdate,
    user: current_user,
    db: db_depends,
):
    correct_data = data.model_dump(exclude_unset=True)
    crud.update_user(
        user_id=user.get("user_id"),
        update_info=correct_data,
        db=db,
    )

    return {"message": "success update"}


@users_router.get(
    "/users-list/{user_id}",
    response_model=UserRead,
    response_model_exclude_none=True,
    response_model_exclude=["role", "is_active", "join_at"],
)
async def retrieve_user(user_id: int, current_user: current_user, db: db_depends):
    user = crud.retrieve_user(user_id, db)

    return user


@users_router.delete("/me")
async def delete_me(user: current_user, db: db_depends):
    user_id = user.get("user_id")
    crud.delete_user(user_id, db)

    return {"message": "delete success"}


@users_router.delete("/user-list/{user_id}")
async def delete_user(user_id: int, user: current_user, db: db_depends):
    if user.get("role") not in [Role.ADMIN, Role.STAFF]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="you dont have permission"
        )

    crud.delete_user(user_id, db)

    return {"message": "delete success"}
