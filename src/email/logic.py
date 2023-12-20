from fastapi_mail import ConnectionConfig, MessageSchema, FastMail, MessageType
from jose import jwt
from jose.exceptions import JWTError
from database.settings import SECRET_KEY
from src.users.models import User
from database.depends import db_depends
from datetime import timedelta, datetime

from .config import mail_config

db = db_depends()


class SendMail:
    async def send_email(self, email):
        mail = FastMail(mail_config)

        token = self._create_token_for_confirm(email, minutes=600)

        link = f"http://127.0.0.1:8000/email/confirm/{token}"

        html = f"""<p>For your email verification please click link {link} </p> """

        message = MessageSchema(
            recipients=[email],
            subject="Hello",
            subtype="html",
            body=html,
        )

        await mail.send_message(message)

    def check_token_and_verify(self, token):
        try:
            token_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except JWTError:
            return "Incorrect data"
        date = datetime.fromtimestamp(token_data.get("exp"))
        if date < datetime.now():
            raise JWTError()

        current_user = (
            db.query(User).filter(User.email == token_data.get("email")).one_or_none()
        )

        self._change_to_active(current_user)

    def _change_to_active(self, user):
        user.is_active = True

        db.commit()

    @classmethod
    def _create_token_for_confirm(cls, email, minutes):
        exp = datetime.now() + timedelta(minutes=minutes)
        data = {"email": email, "exp": exp}
        token = jwt.encode(data, SECRET_KEY, algorithm="HS256")

        return token
