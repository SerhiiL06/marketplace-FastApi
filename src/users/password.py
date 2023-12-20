from passlib.context import CryptContext
from fastapi_mail import FastMail, MessageSchema
from src.email.config import mail_config
from src.email.logic import SendMail

create_token = SendMail()


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
