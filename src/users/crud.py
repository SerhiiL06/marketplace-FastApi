from .models import User

from database import settings
from database.depends import db_depends
from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from .exceptions import UserAlreadyExists, PasswordDifference
from jose import jwt
from jose.exceptions import JWTError
from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

bcrypt = CryptContext(schemes=["bcrypt"])


bearer_token = OAuth2PasswordBearer(tokenUrl="users/token")


class UserCRUD:
    def create_user(self, user_data):
        if db_depends.query(User).filter(User.email == user_data.email).first():
            raise UserAlreadyExists(email=user_data.email)

        if user_data.password1 != user_data.password2:
            raise PasswordDifference()

        password = bcrypt.hash(user_data.password1)

        new_user = User(
            **user_data.model_dump(exclude=["password1", "password2"]),
            hashed_password=password
        )

        db_depends.add(new_user)
        db_depends.commit()

        return True
