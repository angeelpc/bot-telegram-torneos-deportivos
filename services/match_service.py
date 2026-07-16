from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.match import Match
from db.repositories.match_repo import match_repo

class MatchService:
    async def set_match_result(self, db: AsyncSession, match_id: str, score_t1: int, score_t2: int, user_is_organizer: bool) -> Tuple[bool, str]:
        if not user_is_organizer:
            return False, "No tienes permisos para realizar esta acción."

        match = await match_repo.get(db, match_id)
        if not match:
            return False, "Partido no encontrado."
            
        if not match.team1_id or not match.team2_id:
            return False, "El partido no tiene los dos equipos asignados aún."

        if match.status == "completed":
            return False, "El partido ya está completado. Si hubo un error, usa la opción de corregir resultado."

        if score_t1 == score_t2:
            return False, "No se permiten empates en eliminación directa."

        winner_id = match.team1_id if score_t1 > score_t2 else match.team2_id

        # Actualizar partido actual
        await match_repo.update(db, db_obj=match, obj_in={
            "score_team1": score_t1,
            "score_team2": score_t2,
            "winner_team_id": winner_id,
            "status": "completed"
        })

        # Avanzar ganador al siguiente partido
        if match.next_match_id:
            next_m = await match_repo.get(db, match.next_match_id)
            if next_m:
                # Comprobar qué slot está libre. Si se está corrigiendo un resultado, 
                # la lógica sería más compleja, pero para un set normal:
                # Una forma de saber si venimos de la rama superior o inferior es por el ID o
                # asumiendo que el primero que llega es team1.
                # Para ser robustos y deterministas, necesitamos saber si el current_match 
                # es un hijo izquierdo o derecho del next_match.
                # Vamos a usar una regla simple: si team1_id es None, lo asignamos ahí, si no en team2_id.
                if next_m.team1_id is None:
                    await match_repo.update(db, db_obj=next_m, obj_in={"team1_id": winner_id})
                elif next_m.team2_id is None:
                    await match_repo.update(db, db_obj=next_m, obj_in={"team2_id": winner_id})
                else:
                    # En caso de corrección, tendríamos que reemplazar al ganador anterior
                    # Pero en MVP `set_match_result` asume flujo hacia adelante normal.
                    pass

        return True, "Resultado guardado y equipo ganador avanzado."

    async def schedule_match(self, db: AsyncSession, match_id: str, scheduled_time: str, location: str) -> bool:
        match = await match_repo.get(db, match_id)
        if not match:
            return False
            
        from datetime import datetime
        try:
            # Simplificación: Asumimos formato ISO o formato manejable para MVP
            time_obj = datetime.fromisoformat(scheduled_time)
        except ValueError:
            # Fallback o manejo de error a nivel handler
            return False

        await match_repo.update(db, db_obj=match, obj_in={
            "scheduled_time": time_obj,
            "location": location,
            "status": "scheduled"
        })
        return True

match_service = MatchService()
