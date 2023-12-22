from typing import Annotated

from fastapi import APIRouter, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import desc
from .password import PasswordFeature

from src.advertisements.crud import AdvertisementsCRUD


from .authentication import UserAuth, current_user, decode_token
from .crud import BookmarkActions, UserCRUD
from .schemes import (
    ChangePassword,
    DefaultUserUpdate,
    RegisterUser,
    Token,
    UserRead,
    AbstractUser,
    ForgotPasswordScheme,
)


users_router = APIRouter(prefix="/users")

adv_crud = AdvertisementsCRUD()

bookmark = BookmarkActions()


# register/login endpoints
@users_router.post(
    "/register",
    tags=["register/login"],
    description="the login endpoint",
    response_model=AbstractUser,
    status_code=status.HTTP_201_CREATED,
    response_description="user success created",
)
async def register(data: RegisterUser, crud: UserCRUD = Depends(UserCRUD)):
    return await crud.create_user(data)


@users_router.post(
    "/token",
    tags=["register/login"],
    description="In this endpoint create access token for user. Use this only for depends",
    response_model=Token,
    response_description="return JWT token",
)
async def token_login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: UserAuth = Depends(UserAuth),
):
    return auth.login(data)


@users_router.post("/change-password")
async def change_password(
    password_data: ChangePassword,
    user: current_user,
    crud: UserCRUD = Depends(UserCRUD),
):
    crud.change_password(token_data=user, password=password_data)

    return Response(content="password update", status_code=status.HTTP_200_OK)


# user profile endpoints
@users_router.get(
    "/me",
    tags=["user profile"],
    summary="user can see her profile use this endpoint",
    response_model=UserRead,
    response_model_exclude=["id", "is_active", "role", "join_at"],
)
async def my_profile(
    user: current_user,
    crud: UserCRUD = Depends(UserCRUD),
):
    data = crud.retrieve_user(user.get("user_id"))
    return data


@users_router.patch(
    "/me", tags=["user profile", "user CRUD"], description="user can update his profile"
)
async def update_user(
    data: DefaultUserUpdate,
    user: current_user,
    crud: UserCRUD = Depends(UserCRUD),
):
    currect_data = data.model_dump(exclude_unset=True)
    update_user = crud.update_user(
        user_id=user.get("user_id"),
        update_info=currect_data,
    )

    return Response(content={"user": update_user}, status_code=status.HTTP_200_OK)


# retrieve user
@users_router.get(
    "/users-list/{user_id}",
    tags=["users CRUD"],
    response_model=UserRead,
    response_model_exclude_none=True,
    response_model_exclude=["role", "is_active", "join_at"],
    description="user profile view",
)
async def retrieve_user(
    user_id: int,
    crud: UserCRUD = Depends(UserCRUD),
):
    user = crud.retrieve_user(user_id)

    return user


@users_router.delete(
    "/me", tags=["users CRUD"], description="user can delete his account"
)
async def delete_me(
    user: current_user,
    crud: UserCRUD = Depends(UserCRUD),
):
    crud.delete_user(user)

    return Response(content="user was deleted", status_code=status.HTTP_200_OK)


@users_router.post("/update-password/{token}", tags=["forgot password"])
async def update_password(
    token: str,
    password_data: ForgotPasswordScheme,
    pwd: PasswordFeature = Depends(PasswordFeature),
):
    pwd.change_password(token, password_data)


mail = SendMail()


@users_router.get("/confirm/{token}", tags=["forgot password"])
async def link_for_verification(token: str):
    mail.check_token_and_verify(token)

    return {"message": "Your email was confirm"}


@users_router.post("/forgot-password/", tags=["forgot password"])
async def forgot_password_send_email(email: EmailStr, db: db_depends):
    chech_exists = db.query(User).filter(User.email == email).one_or_none()

    if chech_exists is None:
        raise UserIDError(email)

    await forgot_password(email)
