import asyncio
import sys
import os

# Asegurar que python encuentre el módulo principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import AsyncSessionLocal
from db.repositories.user_repo import user_repo
from db.repositories.team_repo import team_repo
from db.repositories.category_repo import category_repo

FAKE_TEAMS = [
    "Deportivo Demo",
    "Los Galácticos",
    "Atlético Prueba",
    "Sporting Falso",
    "Real Mock",
    "Club Seed",
    "Demo FC",
    "Unión Test"
]

async def seed_data(category_id: str):
    print(f"🌱 Iniciando sembrado de datos en la Categoría: {category_id}")
    
    async with AsyncSessionLocal() as db:
        # Validar que la categoría exista
        category = await category_repo.get_by_id(db, category_id)
        if not category:
            print("❌ ERROR: La categoría especificada no existe en la base de datos.")
            return

        print(f"✅ Categoría encontrada: {category.name}")
        
        # Inyectar usuarios y equipos
        base_telegram_id = 1000000 # IDs ficticios
        for i, team_name in enumerate(FAKE_TEAMS):
            fake_tg_id = base_telegram_id + i
            fake_name = f"Capitán {team_name}"
            
            # Crear o buscar usuario ficticio
            user = await user_repo.get_by_telegram_id(db, fake_tg_id)
            if not user:
                user = await user_repo.create(db, obj_in={
                    "telegram_id": fake_tg_id,
                    "full_name": fake_name
                })
                
            # Crear equipo en la categoría
            team = await team_repo.create(db, obj_in={
                "category_id": category_id,
                "name": team_name,
                "captain_id": user.id,
                "status": "approved"
            })
            print(f"  + Equipo inyectado: {team_name} (Capitán: {fake_name})")

        print("🎉 ¡Sembrado exitoso! 8 Equipos creados y aprobados.")
        print("💡 Instrucciones para tu DEMO:")
        print("   1. Ve a tu bot de Telegram.")
        print("   2. Si el torneo sigue en registro, usa tu menú de Organizador para 'Cerrar Registros'.")
        print("   3. Pulsa 'Generar Bracket'.")
        print("   4. ¡Sorprende a tu cliente mostrando cómo se arma el torneo automáticamente!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ ERROR: Faltan argumentos.")
        print("👉 Uso correcto: python scripts/seed_demo.py <ID_DE_LA_CATEGORIA>")
        print("💡 Tip: Puedes obtener el ID de la categoría revisando la URL del botón de registro o la base de datos.")
    else:
        category_id = sys.argv[1]
        asyncio.run(seed_data(category_id))
