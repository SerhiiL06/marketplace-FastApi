from fastapi import APIRouter, Query, Response, status, Depends

from database.depends import db_depends
from src.users.admin import check_role
from src.users.authentication import current_user

from .crud import AdvertisementsCRUD
from .schemes import AdvertisementsScheme, UpdateAdvScheme

adv_router = APIRouter(prefix="/board", tags=["advertisements"])


@adv_router.post(
    "/create",
    response_model=AdvertisementsScheme,
    summary="Authentication users can create adv",
)
async def post_adv(
    data: AdvertisementsScheme,
    user: current_user,
    crud: AdvertisementsCRUD = Depends(AdvertisementsCRUD),
):
    return crud.create_adv(data, user)


@adv_router.get(
    "/list",
    response_model=list[AdvertisementsScheme],
    response_model_exclude_none=True,
    summary="catalog of adv",
    description="Auth users and auth can see catalog of adv. And can filters.",
)
async def get_all_adv(
    category: list[str] = Query(None),
    title: str = Query(None),
    crud: AdvertisementsCRUD = Depends(AdvertisementsCRUD),
):
    filter_data = {"title": title, "category": category}
    return crud.list_adv(**filter_data)


@adv_router.get(
    "/my-adv",
    response_model=list[AdvertisementsScheme],
    response_model_exclude_none=True,
)
async def my_adv(
    user: current_user, crud: AdvertisementsCRUD = Depends(AdvertisementsCRUD)
):
    return crud.my_adv_list(user)


@adv_router.get(
    "/{adv_id}", response_model=AdvertisementsScheme, response_model_exclude_none=True
)
async def get_adv(adv_id: int, crud: AdvertisementsCRUD = Depends(AdvertisementsCRUD)):
    return crud.retrieve(adv_id)


@adv_router.put("/{adv_id}")
async def update_adv(
    adv_id: int,
    db: db_depends,
    user: current_user,
    update_info: UpdateAdvScheme,
    crud: AdvertisementsCRUD = Depends(AdvertisementsCRUD),
):
    crud.update_adv(db, adv_id, user, update_info)

    return Response(status_code=status.HTTP_200_OK)


@adv_router.delete("/{adv_id}")
@check_role(["default", "admin", "staff"])
async def delete_adv(
    avd_id: int,
    user: current_user,
    crud: AdvertisementsCRUD = Depends(AdvertisementsCRUD),
):
    crud.delete(avd_id, user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
