from fastapi import APIRouter, Depends, HTTPException, status, Response

from .schemes import RegisterSuperUser, UserRead

from .crud import UserCRUD
from .models import User
from .authentication import UserAuth, current_user

from database.depends import db_depends
from .exceptions import UserIDError


admin_router = APIRouter(prefix="/admin/users", tags=["admin users"])


@admin_router.get("/users/all", response_model=list[UserRead])
async def user_list(user: current_user, db: db_depends):
    if user.get("role") not in ["admin", "staff"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    crud = UserCRUD()

    query = crud.user_list(db)

    return query


@admin_router.get("/users/{user_id}", response_model=UserRead)
async def retrieve_user(user_id: int, db: db_depends, user: current_user):
    if user.get("role") not in ["admin", "staff"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    crud = UserCRUD()

    retrieve = crud.retrieve_user(user_id, db)

    return retrieve


@admin_router.post("/create-superuser")
async def create_superuser(data: RegisterSuperUser, user: current_user, db: db_depends):
    auth = UserAuth()

    if user.get("role") not in ["admin", "staff"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    auth._create_superuser(data=data, db=db)

    return Response(content="superuser create", status_code=status.HTTP_201_CREATED)


@admin_router.delete("/user-list/{user_id}")
async def delete_user(user_id: int, user: current_user, db: db_depends):
    if user.get("role") not in ["admin", "staff"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    user_to_delete = db.query(User).filter(User.id == user_id).one_or_none()

    if user_to_delete is None:
        raise UserIDError(user_id)

    if user_to_delete.role in ["admin", "staff"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you cannot delete member with this status sorry!",
        )

    db.delete(user_to_delete)

    db.commit()

    return Response(content="success delete", status_code=status.HTTP_204_NO_CONTENT)
