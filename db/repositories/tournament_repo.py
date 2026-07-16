from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.tournament import Tournament
from db.repositories.base import BaseRepository

class TournamentRepository(BaseRepository[Tournament]):
    async def get_by_organizer(self, db: AsyncSession, organizer_id: str) -> List[Tournament]:
        query = select(self.model).where(self.model.organizer_id == organizer_id)
        result = await db.execute(query)
        return result.scalars().all()

tournament_repo = TournamentRepository(Tournament)
