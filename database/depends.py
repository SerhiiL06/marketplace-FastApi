from fastapi import Depends
from typing import Annotated
from .settings import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_depends = Annotated[SessionLocal, Depends(get_db)]
