from pydantic import BaseModel, ConfigDict, Field, EmailStr, validator
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class Role(Enum):
    DEFAULT = "default"
    STAFF = "staff"
    ADMIN = "admin"


class AbstractUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr = Field()


# Register/Login/ChangePassword Opertions


class RegisterUser(AbstractUser):
    first_name: str = Field(min_length=5, max_length=15)
    last_name: str = Field(min_length=5, max_length=15)
    password1: str = Field(min_length=6, title="password")
    password2: str = Field(min_length=6, title="confirm password")


class LoginUser(AbstractUser):
    password: str


class ChangePassword(LoginUser):
    new_password1: str = Field(min_length=6)
    new_password2: str = Field(min_length=6)


# READ/UPDATE OPERATIONS


class DefaultUserRead(AbstractUser):
    id: int
    first_name: str
    last_name: str
    company: Optional[str] = None
    logo: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None


class AdminUserRead(DefaultUserRead):
    role: Optional[Literal[Role.ADMIN, Role.STAFF, Role.DEFAULT]] = Field(
        default="default"
    )
    is_active: bool
    join_at: datetime


class UserUpdate(DefaultUserRead):
    role: Optional[Literal[Role.ADMIN, Role.STAFF, Role.DEFAULT]] = Field(
        default="default"
    )
    is_active: bool = None
