from fastapi import HTTPException, status
from database.depends import db_depends

from .exceptions import AdvIDNotExists
from .models import Advertisements, Car, House, Work


class AdvertisementsCRUD:
    def create_adv(self, data, user, db=db_depends):
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
            new = House(**data.house_info.model_dump(), advertisement=obj.id)

            obj.house_info = new

        elif data.type == "car":
            new = Car(**data.car_info.model_dump(), advertisement=obj.id)
            obj.car_info = new

        elif data.type == "work":
            new = Work(**data.work_info.model_dump(), advertisement=obj.id)
            obj.car_info = new

        db.add(new)

        db.commit()

        return new

    def update_adv(self, adv_id, user, update_data, db=db_depends):
        current_obj = db.query(Advertisements).get(adv_id)
        if current_obj is None:
            raise AdvIDNotExists(adv_id)
        if current_obj.owner != user.get("user_id"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        data = update_data.model_dump(exclude_none=True)
        house_info = data.pop("house_info", None)
        car_info = data.pop("car_info", None)
        work_info = data.pop("work_info", None)

        type_obj = house_info or car_info or work_info

        for k, v in data.items():
            setattr(current_obj, k, v)

        if house_info:
            children = db.query(House).get(current_obj.house_info.id)

        elif car_info:
            children = db.query(Car).get(current_obj.car_info.id)

        elif work_info:
            children = db.query(Work).get(current_obj.work_info.id)

        for k, v in type_obj.items():
            setattr(children, k, v)

        db.commit()

    def list_adv(
        self,
        db=db_depends,
        **filter_data,
    ):
        db = db_depends()
        object_list = db.query(Advertisements).join(
            [
                Advertisements.car_info,
            ]
        )
        if filter_data.get("category", None) is not None:
            object_list = object_list.filter(
                (Advertisements.type).in_(filter_data.get("category"))
            )

        if filter_data.get("title", None) is not None:
            object_list = object_list.filter(
                (Advertisements.title).icontains(filter_data.get("title"))
            )

        return object_list.all()

    def retrieve(self, adv_id, db=db_depends):
        obj = db.query(Advertisements).filter(Advertisements.id == adv_id).one_or_none()
        if obj is None:
            raise AdvIDNotExists(adv_id)
        return obj

    def delete(self, db, obj_id, user):
        obj = self.retrieve(db, obj_id)

        if user.get("role") == "default":
            if obj.owner != user.get("user_id"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Don't have permision"
                )

        db.delete(obj)

        db.commit()

    def my_adv_list(self, user, db=db_depends):
        object_list = db.query(Advertisements).filter(
            Advertisements.owner == user.get("user_id")
        )

        return object_list if object_list else []
