from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.category import Category
from typing import List

class CategoryRepository:
    async def create(self, db: AsyncSession, tournament_id: str, name: str) -> Category:
        category = Category(tournament_id=tournament_id, name=name)
        db.add(category)
        await db.commit()
        await db.refresh(category)
        return category

    async def get_by_id(self, db: AsyncSession, category_id: str) -> Category:
        result = await db.execute(select(Category).where(Category.id == category_id))
        return result.scalars().first()

    async def get_by_tournament(self, db: AsyncSession, tournament_id: str) -> List[Category]:
        result = await db.execute(select(Category).where(Category.tournament_id == tournament_id))
        return list(result.scalars().all())

category_repo = CategoryRepository()
