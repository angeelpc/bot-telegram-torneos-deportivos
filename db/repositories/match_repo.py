from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from db.models.match import Match, Round
from db.repositories.base import BaseRepository

class MatchRepository(BaseRepository[Match]):
    async def get_matches_by_category(self, db: AsyncSession, category_id: str) -> List[Match]:
        query = select(self.model).join(Round).where(
            self.model.category_id == category_id
        ).options(
            joinedload(self.model.team1),
            joinedload(self.model.team2),
            joinedload(self.model.round)
        ).order_by(Round.round_number, self.model.created_at)
        result = await db.execute(query)
        return result.scalars().all()

match_repo = MatchRepository(Match)

class RoundRepository(BaseRepository[Round]):
    async def get_rounds_by_category(self, db: AsyncSession, category_id: str) -> List[Round]:
        query = select(self.model).where(
            self.model.category_id == category_id
        ).order_by(self.model.round_number)
        result = await db.execute(query)
        return result.scalars().all()

round_repo = RoundRepository(Round)
