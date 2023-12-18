from fastapi import APIRouter, Query
from .schemes import AdvertisementsScheme
from src.users.authentication import current_user
from database.depends import db_depends
from .crud import AdvertisementsCRUD


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
    "/{adv_id}", response_model=AdvertisementsScheme, response_model_exclude_none=True
)
async def get_adv(db: db_depends, adv_id: int):
    return crud.retrieve(db, adv_id)
