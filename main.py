from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.users.routers import users_router
from src.users.admin import admin_router
from src.advertisements.routers import adv_router
from src.users.exceptions import UserAlreadyExists, PasswordDifference, UserIDError

app = FastAPI(title="Marketplace", version="0.0.1")


# connect routers
app.include_router(users_router)


app.include_router(admin_router)

app.include_router(adv_router)

# register exceptions


@app.exception_handler(UserAlreadyExists)
async def user_exists_handler(request: Request, exc: UserAlreadyExists):
    return JSONResponse(
        content=f"user with this email {exc.email} alredy exists",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.exception_handler(PasswordDifference)
async def password_error(request: Request, exc: PasswordDifference):
    return JSONResponse(
        content="password must be the same!",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


@app.exception_handler(UserIDError)
async def password_error(request: Request, exc: UserIDError):
    return JSONResponse(
        content=f"user with ID {exc.id} doesn't exists",
        status_code=status.HTTP_404_NOT_FOUND,
    )
