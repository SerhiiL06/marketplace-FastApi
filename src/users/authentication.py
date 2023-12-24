from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext

from database import settings
from database.depends import db_depends

from .crud import UserCRUD
from .models import User

bcrypt = CryptContext(schemes=["bcrypt"])


bearer_token = OAuth2PasswordBearer(tokenUrl="users/token")


class UserAuth:
    def login(self, data, db: db_depends):
        db = db_depends()
        user = db.query(User).filter(User.email == data.username).first()

        # check email address
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect email"
            )

        # verify password

        verify_password = bcrypt.verify(data.password, user.hashed_password)

        if not verify_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="incorrect password"
            )

        if user.is_active == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="you need to verify or profile",
            )

        token = self._create_access_token(user.role, user.id, user.email)

        return {"access_token": token, "token_type": "bearer"}

    def _create_superuser(self, data: dict, db):
        crud = UserCRUD()

        crud.create_user(user_data=data, db=db, admin=True)

    @classmethod
    def _create_access_token(cls, role: str, id: int, email: str):
        payload = {"user_id": id, "role": role, "email": "email"}

        exp = datetime.utcnow() + timedelta(minutes=20)

        payload.update({"exp": exp})

        token = jwt.encode(claims=payload, key=settings.SECRET_KEY, algorithm="HS256")

        return token


def decode_token(token):
    user = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    exp = datetime.fromtimestamp(user.get("exp"))
    if exp < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return user


def authenticate(token: Annotated[str, Depends(bearer_token)]):
    if token is None:
        raise JWTError()

    return decode_token(token)


current_user = Annotated[dict, Depends(authenticate)]
