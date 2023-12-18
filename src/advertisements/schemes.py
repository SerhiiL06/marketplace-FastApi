from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional, Union
from datetime import datetime


class CarScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    brand: Literal["BMW", "Mersedes", "Audi"]
    year: int = Field(gt=1900, lt=datetime.now().year + 1)
    engine_power: float = Field(gt=0, lt=10)
    status: Literal["new", "in_use"]
    color: Optional[Literal["black", "white", "red"]] = None


class HouseScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    rooms: int = Field(gt=0, lt=10)
    area: Union[int, float] = Field(gt=0, lt=5000)


class WorkScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type_of_work: Literal["local", "remote"]


class AdvertisementsScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str = Field(min_length=5, max_length=50)
    description: str = Field(min_length=5, max_length=150)

    price: float = Field(gt=0)

    type: Literal["work", "car", "other", "house"]

    is_publish: bool = Field(default=True)

    town: Literal["Kyiv", "Berlin", "New York"]

    car_info: Optional[CarScheme] = None
    house_info: Optional[HouseScheme] = None
    work_info: Optional[WorkScheme] = None
