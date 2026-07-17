from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.team import Team
from db.repositories.base import BaseRepository

class TeamRepository(BaseRepository[Team]):
    async def get_by_category(self, db: AsyncSession, category_id: str) -> List[Team]:
        query = select(self.model).where(self.model.category_id == category_id)
        result = await db.execute(query)
        return result.scalars().all()
        
    async def get_approved_teams(self, db: AsyncSession, category_id: str) -> List[Team]:
        query = select(self.model).where(
            self.model.category_id == category_id,
            self.model.status == "approved"
        )
        result = await db.execute(query)
        return result.scalars().all()

team_repo = TeamRepository(Team)
