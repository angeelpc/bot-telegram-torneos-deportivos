from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.user import User
from db.repositories.base import BaseRepository

class UserRepository(BaseRepository[User]):
    async def get_by_telegram_id(self, db: AsyncSession, telegram_id: int) -> Optional[User]:
        query = select(self.model).where(self.model.telegram_id == telegram_id)
        result = await db.execute(query)
        return result.scalars().first()

user_repo = UserRepository(User)
