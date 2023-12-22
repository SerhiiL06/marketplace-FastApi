from fastapi_mail import FastMail, MessageSchema
from src.users.models import User
from database.depends import db_depends
from fastapi import HTTPException, status
from src.email.config import mail_config
from src.email.logic import SendMail
from .exceptions import PasswordDifference
from passlib.context import CryptContext
from authentication import decode_token

create_token = SendMail()

bcrypt = CryptContext(schemes=["bcrypt"])


class HashPassword:
    BCTYPE = CryptContext(schemes=["bcrypt"])

    @staticmethod
    def hash_password(password):
        return HashPassword.hash(password)

    @staticmethod
    def verify_password(secret, hashed):
        result = HashPassword.verify(secret, hashed)
        if result is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="check you old password"
            )


class PasswordFeature:
    def __init__(self, bctype: HashPassword) -> None:
        self.bctype = bcrypt

    # check_password = HashPassword()

    def change_password(self, token_data, password):
        db = db_depends()
        token = decode_token(token_data)
        current_user = (
            db.query(User).filter(User.id == token.get("user_id")).one_or_none()
        )

        if current_user is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="something went wrong"
            )

        # check user password
        self.bctype.verify(password.old_password, current_user.hashed_password)

        if password.new_password1 != password.new_password2:
            raise PasswordDifference()

        current_user.hashed_password = self.bctype.hash_password(password.new_password1)

        db.commit()


async def forgot_password(email):
    mail = FastMail(mail_config)

    token = create_token._create_token_for_confirm(email, minutes=20)
    link = f"http://127.0.0.1:8000/email/update-password/{token}"

    html = f"""<p>For change your password click here {link} </p> """

    message = MessageSchema(
        recipients=[email],
        subject="Hello",
        subtype="html",
        body=html,
    )

    await mail.send_message(message)
