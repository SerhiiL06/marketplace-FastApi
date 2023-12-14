from database.settings import Base
from sqlalchemy import String, Integer, Boolean, DateTime, LargeBinary, MetaData
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    hashed_password: Mapped[str] = mapped_column(String)

    role: Mapped[str] = mapped_column(String, default="simple")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    join_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    company: Mapped[str] = mapped_column(String(50), nullable=True)

    logo: Mapped[str] = mapped_column(LargeBinary, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=True, unique=True)

    city: Mapped[str] = mapped_column(String(20), nullable=True)
