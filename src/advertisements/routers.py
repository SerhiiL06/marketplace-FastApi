from fastapi import APIRouter, Query, Response, status

from database.depends import db_depends
from src.users.admin import check_role
from src.users.authentication import current_user

from .crud import AdvertisementsCRUD
from .schemes import AdvertisementsScheme, UpdateAdvScheme

adv_router = APIRouter(prefix="/board", tags=["advertisements"])

crud = AdvertisementsCRUD()


@adv_router.post("/create")
async def post_adv(data: AdvertisementsScheme, db: db_depends, user: current_user):
    crud.create_adv(data, user, db)
    return {"message": "well done"}


@adv_router.get(
    "/list", response_model=list[AdvertisementsScheme], response_model_exclude_none=True
)
async def get_all_adv(
    db: db_depends, category: list[str] = Query(None), title: str = Query(None)
):
    filter_data = {"title": title, "category": category}
    return crud.list_adv(db, **filter_data)


@adv_router.get(
    "/my-adv",
    response_model=list[AdvertisementsScheme],
    response_model_exclude_none=True,
)
async def my_adv(db: db_depends, user: current_user):
    obj_list = crud.my_adv_list(db, user)

    if obj_list:
        return obj_list

    return Response(
        content={"now you don't have any advertisements"},
        status_code=status.HTTP_204_NO_CONTENT,
    )


@adv_router.get(
    "/{adv_id}", response_model=AdvertisementsScheme, response_model_exclude_none=True
)
async def get_adv(db: db_depends, adv_id: int):
    return crud.retrieve(db, adv_id)


@adv_router.put("/{adv_id}")
async def update_adv(
    adv_id: int, db: db_depends, user: current_user, update_info: UpdateAdvScheme
):
    crud.update_adv(db, adv_id, user, update_info)

    return Response(status_code=status.HTTP_200_OK)


@adv_router.delete("/{adv_id}")
@check_role(["default", "admin", "staff"])
async def delete_adv(db: db_depends, avd_id: int, user: current_user):
    crud.delete(db, avd_id, user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
