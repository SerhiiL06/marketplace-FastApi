from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    token_type: str


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
    password1: str = Field(min_length=6, description="password")
    password2: str = Field(min_length=6, description="confirm password")


class LoginUser(AbstractUser):
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password1: str = Field(min_length=6)
    new_password2: str = Field(min_length=6)


# READ/UPDATE OPERATIONS


class UserRead(AbstractUser):
    id: int
    first_name: str
    last_name: str
    company: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    role: Literal[Role.ADMIN, Role.STAFF, Role.DEFAULT] = Field(default="default")
    is_active: bool
    join_at: datetime


class DefaultUserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    logo: Optional[bytes] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None

    # Дані для перевірки


class AdminUserUpdate(DefaultUserUpdate):
    role: Optional[Literal[Role.ADMIN, Role.STAFF, Role.DEFAULT]] = Field(
        default="default"
    )
    is_active: bool = None
