from fastapi import FastAPI

# from database.settings import Base, engine
# from src.users.models import User


app = FastAPI(title="Marketplace", version="0.0.1")


@app.get("/")
async def hello():
    return {"message": "hello world"}
