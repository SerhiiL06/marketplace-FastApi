from datetime import datetime
from enum import Enum
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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
    model_config = ConfigDict(from_attributes=True)
    first_name: str = Field(min_length=5, max_length=15)
    last_name: str = Field(min_length=5, max_length=15)
    password1: str = Field(min_length=6, description="password")
    password2: str = Field(min_length=6, description="confirm password")


class RegisterSuperUser(RegisterUser):
    role: Optional[Literal[Role.ADMIN, Role.STAFF]] = Field(default=Role.STAFF.value)


class LoginUser(AbstractUser):
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password1: str = Field(min_length=6)
    new_password2: str = Field(min_length=6)


class ForgotPasswordScheme(BaseModel):
    password1: str = Field(min_length=6)
    password2: str = Field(min_length=6)


# READ/UPDATE OPERATIONS


class BookmarkScheme(BaseModel):
    adv_id: int


class UserRead(AbstractUser):
    id: int
    first_name: str
    last_name: str
    company: Optional[str] = None
    phone_number: Optional[str] = None
    city: Optional[str] = None
    role: Literal["admin", "staff", "default"] = Field(default="default")
    is_active: bool
    join_at: datetime

    bookmarks: list[BookmarkScheme]


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


class MyBookmarksScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
