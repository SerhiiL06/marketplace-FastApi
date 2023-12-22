from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.settings import Base


class Advertisements(Base):
    __tablename__ = "advertisements"
    owner: Mapped[int] = mapped_column(ForeignKey("users.id"))

    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column()
    image: Mapped[str] = mapped_column(nullable=True)
    created: Mapped[datetime] = mapped_column(default=datetime.now)
    type: Mapped[str] = mapped_column()

    is_publish: Mapped[bool] = mapped_column(default=True)

    town: Mapped[str] = mapped_column(nullable=True)

    house_info: Mapped["House"] = relationship(
        back_populates="type_info", cascade="all, delete-orphan", uselist=False
    )
    work_info: Mapped["Work"] = relationship(
        back_populates="type_info", cascade="all, delete-orphan", uselist=False
    )
    car_info: Mapped["Car"] = relationship(
        back_populates="type_info", cascade="all, delete-orphan", uselist=False
    )

    bookmarks: Mapped["Bookmark"] = relationship(back_populates="advertisement")
    __table_args__ = (UniqueConstraint("title"),)


class House(Base):
    __tablename__ = "houses"
    advertisement: Mapped[int] = mapped_column(
        ForeignKey("advertisements.id", ondelete="CASCADE")
    )
    rooms: Mapped[int] = mapped_column()
    area: Mapped[float] = mapped_column()

    type_info: Mapped["Advertisements"] = relationship(
        back_populates="house_info", single_parent=True, cascade="all, delete-orphan"
    )


class Car(Base):
    __tablename__ = "cars"
    advertisement: Mapped[int] = mapped_column(
        ForeignKey("advertisements.id", ondelete="CASCADE")
    )
    brand: Mapped[str] = mapped_column()
    year: Mapped[int] = mapped_column()
    engine_power: Mapped[float] = mapped_column()
    color: Mapped[str] = mapped_column(nullable=True)

    status: Mapped[str] = mapped_column()

    type_info: Mapped["Advertisements"] = relationship(
        back_populates="car_info", single_parent=True, cascade="all, delete-orphan"
    )


class Work(Base):
    __tablename__ = "works"
    advertisement: Mapped[int] = mapped_column(
        ForeignKey("advertisements.id", ondelete="CASCADE")
    )
    type_of_work: Mapped[str] = mapped_column()

    type_info: Mapped["Advertisements"] = relationship(
        back_populates="work_info", single_parent=True, cascade="all, delete-orphan"
    )
