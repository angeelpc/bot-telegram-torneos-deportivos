from sqlalchemy.ext.asyncio import AsyncSession
from db.repositories.tournament_repo import tournament_repo
from db.repositories.user_repo import user_repo
from db.repositories.category_repo import category_repo

class TournamentService:
    async def create_tournament(self, db: AsyncSession, name: str, description: str, categories_str: str, organizer_telegram_id: int):
        # 1. Buscar al organizador o crearlo
        user = await user_repo.get_by_telegram_id(db, organizer_telegram_id)
        if not user:
            user = await user_repo.create(db, obj_in={"telegram_id": organizer_telegram_id})
            
        # 2. Crear torneo
        tournament = await tournament_repo.create(db, obj_in={
            "name": name,
            "description": description,
            "organizer_id": user.id,
            "status": "registration_open"
        })
        
        # 3. Crear categorías
        categories = []
        for cat_name in categories_str.split(','):
            cat_name = cat_name.strip()
            if cat_name:
                categories.append(await category_repo.create(db, tournament.id, cat_name))
        
        return tournament, categories

    async def close_registration(self, db: AsyncSession, tournament_id: str):
        tournament = await tournament_repo.get(db, tournament_id)
        if not tournament:
            raise ValueError("Torneo no encontrado")
            
        if tournament.status != "registration_open":
            raise ValueError("El torneo no está abierto para registros.")
            
        await tournament_repo.update(db, db_obj=tournament, obj_in={"status": "registration_closed"})
        return True

tournament_service = TournamentService()
