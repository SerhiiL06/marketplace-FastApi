from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi.background import BackgroundTasks

from database import settings
from database.depends import db_depends
from src.email.logic import SendMail
from typing import Annotated

from .exceptions import PasswordDifference, UserAlreadyExists, UserIDError
from .models import Bookmark, Role, User

bcrypt = CryptContext(schemes=["bcrypt"])


bearer_token = OAuth2PasswordBearer(tokenUrl="users/token")


mail = SendMail()


class UserCRUD:
    async def create_user(self, user_data, db=db_depends(), admin=None):
        if db.query(User).filter(User.email == user_data.email).first():
            raise UserAlreadyExists(email=user_data.email)

        if user_data.password1 != user_data.password2:
            raise PasswordDifference()

        password = bcrypt.hash(user_data.password1)

        new_user = User(
            **user_data.model_dump(exclude=["password1", "password2"]),
            hashed_password=password,
            role="default",
            is_active=False
        )

        db.add(new_user)
        db.commit()

        task = BackgroundTasks()

        task.add_task(mail.send_email, new_user)

        return new_user

    def read_users(self, db=db_depends()):
        users = db.query(User)

        return users

    def retrieve_user(self, user_id, db=db_depends()):
        user = (
            db.query(User).join(User.bookmarks).filter(User.id == user_id).one_or_none()
        )

        if user is None:
            raise UserIDError(id=user_id)

        return user

    def update_user(self, user_id, update_info, db=db_depends()):
        user = db.query(User).filter(User.id == user_id).one_or_none()

        for field, value in update_info.items():
            setattr(user, field, value)

        db.commit()

    def delete_user(self, user, db=db_depends()):
        user_id = user.get("user_id")
        user = db.query(User).filter(User.id == user_id).one_or_none()

        if user is None:
            raise UserIDError(id=user_id)

        db.delete(user)

        db.commit()


class BookmarkActions:
    def add_delete_bookmark(self, user, adv_id, db=db_depends()):
        check_exists = (
            db.query(Bookmark)
            .filter(Bookmark.user_id == user.get("user_id"), Bookmark.adv_id == adv_id)
            .one_or_none()
        )

        if check_exists:
            db.delete(check_exists)
            db.commit()
            return Response(content="delete", status_code=status.HTTP_204_NO_CONTENT)

        obj = Bookmark(user_id=user.get("user_id"), adv_id=adv_id)

        db.add(obj)
        db.commit()

        return Response(content="create", status_code=status.HTTP_200_OK)
