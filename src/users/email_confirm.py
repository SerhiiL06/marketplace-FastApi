from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from jose import jwt
from pydantic import EmailStr

from database import settings
from database.depends import db_depends
from src.email.logic import SendMail

from .authentication import bcrypt
from .exceptions import PasswordDifference, UserIDError
from .models import User
from .password import forgot_password
from .schemes import ForgotPasswordScheme

email_router = APIRouter(prefix="/email", tags=["email"])

mail = SendMail()


@email_router.get("/confirm/{token}")
async def email_vericifation(token: str):
    mail.check_token_and_verify(token)

    return {"message": "Your email was confirm"}


@email_router.post("/forgot-password/")
async def forgot_password_email(email: EmailStr, db: db_depends):
    chech_exists = db.query(User).filter(User.email == email).one_or_none()

    if chech_exists is None:
        raise UserIDError(email)

    await forgot_password(email)


@email_router.post("/update-password/{token}")
async def update_password(
    token: str, password_data: ForgotPasswordScheme, db: db_depends
):
    user = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    exp = datetime.fromtimestamp(user.get("exp"))
    if exp < datetime.utcnow():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    current_user = db.query(User).filter(User.email == user.get("email")).one_or_none()

    if password_data.password1 != password_data.password2:
        raise PasswordDifference()

    current_user.hashed_password = bcrypt.hash(password_data.password1)

    db.commit()
