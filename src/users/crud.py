from .models import User, Role

from database import settings
from database.depends import db_depends
from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
from .exceptions import UserAlreadyExists, PasswordDifference, UserIDError
from fastapi.security import OAuth2PasswordBearer

bcrypt = CryptContext(schemes=["bcrypt"])


bearer_token = OAuth2PasswordBearer(tokenUrl="users/token")


class UserCRUD:
    def create_user(self, user_data, db, admin=None):
        if db.query(User).filter(User.email == user_data.email).first():
            raise UserAlreadyExists(email=user_data.email)

        if user_data.password1 != user_data.password2:
            raise PasswordDifference()

        password = bcrypt.hash(user_data.password1)

        new_user = User(
            **user_data.model_dump(exclude=["password1", "password2"]),
            hashed_password=password,
        )

        db.add(new_user)
        db.commit()

    def change_password(self, token_data, password, db):
        current_user = (
            db.query(User).filter(User.id == token_data.get("user_id")).one_or_none()
        )

        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="something went wrong"
            )

        # check user password
        verify_password = bcrypt.verify(
            password.old_password, current_user.hashed_password
        )

        if verify_password is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="check you old password"
            )

        if password.new_password1 != password.new_password2:
            raise PasswordDifference()

        new_hash_password = bcrypt.hash(password.new_password1)

        current_user.hashed_password = new_hash_password

        db.commit()

    def user_list(self, db):
        users = db.query(User)

        return users

    def retrieve_user(self, user_id, db):
        user = db.query(User).filter(User.id == user_id).one_or_none()

        if user is None:
            raise UserIDError(id=user_id)

        return user

    def update_user(self, user_id, update_info, db):
        user = db.query(User).filter(User.id == user_id).one_or_none()

        for field, value in update_info.items():
            setattr(user, field, value)

        db.commit()

    def delete_user(self, user_id, db):
        user = db.query(User).filter(User.id == user_id).one_or_none()

        if user is None:
            raise UserIDError(id=user_id)

        db.delete(user)

        db.commit()
