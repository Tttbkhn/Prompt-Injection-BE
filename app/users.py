from typing import Optional

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin

from db import User, get_user_db

from postmarker.core import PostmarkClient

SECRET = "d0fc29200768eac3010fef523ded1dc67f78a06de9b5adb5c439522bf8bb0fb8"
POSTMARK_SERVER_API_TOKEN = "57ed2191-9ca6-46a3-bcd3-ddc999a73f7e"

postmark = PostmarkClient(
    server_token=POSTMARK_SERVER_API_TOKEN, verbosity=3)


class UserManager(ObjectIDIDMixin, BaseUserManager[User, PydanticObjectId]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")
        template_model = {
            "product_url": "product_url_Value",
            "product_name": "Chatbox Guru",
            "name": user.email,
            "token_reset": f"http://localhost:3000/reset-password?token={token}",
            "company_name": "Computer Science Project Unit",
            "company_address": "Nowherelol"
        }
        postmark.emails.send_with_template(
            From='21870666@student.curtin.edu.au',
            To=user.email,
            TemplateId=37325256,
            TemplateModel=template_model
        )

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(
            f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="api/v2/auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,


)

fastapi_users = FastAPIUsers[User, PydanticObjectId](
    get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
