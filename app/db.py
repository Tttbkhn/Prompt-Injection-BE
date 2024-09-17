import motor.motor_asyncio
from beanie import Document
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase

DATABASE_URL = "mongodb+srv://admin:comp6002@cluster0.hduk4uc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)
db = client["prompt-injection"]


class User(BeanieBaseUser, Document):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)
