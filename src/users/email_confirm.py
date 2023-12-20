from fastapi import APIRouter
from src.email.logic import SendMail

email_router = APIRouter(prefix="/email", tags=["email"])

mail = SendMail()


@email_router.get("/confirm/{token}")
async def email_vericifation(token: str):
    mail.check_token_and_verify(token)

    return {"message": "Your email was confirm"}
