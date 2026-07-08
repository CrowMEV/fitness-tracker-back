from typing import Any, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

import models
from core.security import verify_password
from repositories import UserRepository


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = {
            "user": UserRepository(self.session),
        }

    async def get_users(self) -> Sequence[models.User]:
        return await self.repository["user"].get_items()

    async def get_user_by_id(self, user_id: int) -> models.User | None:
        return await self.repository["user"].get_item_id(user_id)

    async def create_user(self, user_data: dict[str, Any]) -> models.User:
        return await self.repository["user"].create_item(user_data)

    async def update_user(
        self, user_data: dict[str, Any]
    ) -> models.User | None:
        return await self.repository["user"].update_item(user_data)

    async def get_by_email(self, email: str) -> models.User | None:
        return await self.repository["user"].get_by_email(email)

    async def authenticate_user(
        self, email: str, password: str
    ) -> models.User | None:
        user = await self.repository["user"].get_by_email(email)
        if not user or not verify_password(password, user.password):
            return None
        return user
