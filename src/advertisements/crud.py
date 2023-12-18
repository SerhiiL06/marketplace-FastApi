from .models import Advertisements, Car, Work, House
from fastapi import HTTPException, status


class AdvertisementsCRUD:
    def create_adv(self, data, user, db):
        obj = Advertisements(
            **data.model_dump(
                exclude_none=True, exclude=["house_info", "car_info", "work_info"]
            ),
            owner=user.get("user_id"),
        )
        db.add(obj)
        db.commit()

        db.refresh(obj)

        if obj.type == "house":
            new_house = House(**data.house_info.model_dump(), advertisement=obj.id)

            obj.house_info = new_house

            db.add(new_house)

            db.commit()

        elif data.type == "car":
            new_car = Car(**data.car_info.model_dump(), advertisement=obj.id)
            obj.car_info = new_car
            db.add(new_car)
            db.commit()

        elif data.type == "work":
            new_work = Work(**data.work_info.model_dump(), advertisement=obj.id)

            obj.car_info = new_work

            db.add(new_work)

            db.commit()

        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    def list_adv(
        self,
        db,
        **filter_data,
    ):
        object_list = db.query(Advertisements)
        if filter_data.get("category", None) is not None:
            object_list = object_list.filter(
                (Advertisements.type).in_(filter_data.get("category"))
            )

        if filter_data.get("title", None) is not None:
            object_list = object_list.filter(
                (Advertisements.title).icontains(filter_data.get("title"))
            )

        return object_list.all()

    def retrieve(self, db, adv_id):
        obj = db.query(Advertisements).filter(Advertisements.id == adv_id).one_or_none()
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="adv with with id doesn't exists",
            )

        return obj
