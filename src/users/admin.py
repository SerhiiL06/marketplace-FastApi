from fastapi import APIRouter, Depends, HTTPException, status, Response

from .schemes import RegisterSuperUser, UserRead

from .crud import UserCRUD
from .models import User
from .authentication import UserAuth, current_user
from .common import check_role

from database.depends import db_depends
from .exceptions import UserIDError


admin_router = APIRouter(prefix="/admin/users", tags=["admin users"])


@admin_router.get("/users/all", response_model=list[UserRead])
@check_role(allowed_roles=["admin", "staff"])
async def user_list(
    user: current_user, db: db_depends, email: str = None, role: str = None
):
    crud = UserCRUD()

    query = crud.user_list(db)

    if email:
        query = query.filter(User.email == email)

    if role:
        query = query.filter(User.role == role)

    return query


@admin_router.get("/users/{user_id}", response_model=UserRead)
@check_role(allowed_roles=["admin", "staff"])
async def retrieve_user(user_id: int, db: db_depends, user: current_user):
    crud = UserCRUD()

    retrieve = crud.retrieve_user(user_id, db)

    return retrieve


@admin_router.post("/create-superuser")
@check_role(allowed_roles=["admin", "staff"])
async def create_superuser(data: RegisterSuperUser, user: current_user, db: db_depends):
    auth = UserAuth()

    auth._create_superuser(data=data, db=db)

    return Response(content="superuser create", status_code=status.HTTP_201_CREATED)


@admin_router.delete("/user-list/{user_id}")
@check_role(allowed_roles=["admin", "staff"])
async def delete_user(user_id: int, user: current_user, db: db_depends):
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
