from fastapi import APIRouter
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
