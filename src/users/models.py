from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.settings import Base
from src.advertisements.models import Advertisements

from .schemes import Role


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    hashed_password: Mapped[str] = mapped_column(String)

    role: Mapped[str] = mapped_column(default=Role.DEFAULT)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    join_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    company: Mapped[str] = mapped_column(String(50), nullable=True)

    logo: Mapped[str] = mapped_column(LargeBinary, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True, unique=True)

    city: Mapped[str] = mapped_column(String(20), nullable=True)

    bookmarks: Mapped[List["Bookmark"]] = relationship(back_populates="user")


class Bookmark(Base):
    __tablename__ = "bookmarks"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    adv_id: Mapped[int] = mapped_column(
        ForeignKey("advertisements.id"), primary_key=True
    )

    created: Mapped[datetime] = mapped_column(default=datetime.now)

    user: Mapped["User"] = relationship(back_populates="bookmarks")

    advertisement: Mapped["Advertisements"] = relationship(back_populates="bookmarks")
