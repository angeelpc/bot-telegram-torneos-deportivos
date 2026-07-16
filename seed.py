import asyncio
from db.database import AsyncSessionLocal
from db.repositories.user_repo import user_repo
from db.repositories.tournament_repo import tournament_repo
from db.repositories.team_repo import team_repo
from services.bracket_service import bracket_service

async def seed_data():
    async with AsyncSessionLocal() as db:
        print("Creando usuario organizador...")
        organizer = await user_repo.create(db, obj_in={
            "telegram_id": 11111111,
            "full_name": "Admin Organizador"
        })

        print("Creando torneo...")
        tournament = await tournament_repo.create(db, obj_in={
            "name": "Torneo Relámpago MVP",
            "description": "Torneo de prueba con 5 equipos",
            "organizer_id": organizer.id,
            "status": "registration_closed"
        })

        print("Creando equipos...")
        for i in range(1, 6):
            cap = await user_repo.create(db, obj_in={
                "telegram_id": 2000000 + i,
                "full_name": f"Capitán {i}"
            })
            await team_repo.create(db, obj_in={
                "tournament_id": tournament.id,
                "name": f"Equipo {i}",
                "captain_id": cap.id,
                "status": "approved"
            })

        print("Generando bracket...")
        try:
            await bracket_service.generate_bracket(db, tournament.id)
            print("¡Datos generados exitosamente! Revisa tu base de datos para ver el bracket.")
        except Exception as e:
            print(f"Error generando bracket: {e}")

if __name__ == "__main__":
    asyncio.run(seed_data())
