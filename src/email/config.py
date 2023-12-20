from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from dotenv import load_dotenv
import os

load_dotenv()


mail_config = ConnectionConfig(
    MAIL_SERVER=os.getenv("EMAIL_SERVER"),
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL_USER"),
    MAIL_FROM_NAME="marketplace",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    MAIL_PORT=465,
)
