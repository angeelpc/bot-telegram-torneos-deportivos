import math
import random
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.tournament import Tournament
from db.models.team import Team
from db.models.match import Round, Match
from db.repositories.match_repo import round_repo, match_repo
from db.repositories.tournament_repo import tournament_repo
from db.repositories.team_repo import team_repo

class BracketService:
    @staticmethod
    def get_next_power_of_2(n: int) -> int:
        if n == 0:
            return 1
        return 1 << (n - 1).bit_length()

    @staticmethod
    def get_round_name(round_number: int, total_rounds: int) -> str:
        rounds_left = total_rounds - round_number
        if rounds_left == 0:
            return "Final"
        elif rounds_left == 1:
            return "Semifinal"
        elif rounds_left == 2:
            return "Cuartos de final"
        elif rounds_left == 3:
            return "Octavos de final"
        else:
            return f"Ronda {round_number}"

    async def generate_bracket(self, db: AsyncSession, tournament_id: str) -> bool:
        # 1. Validaciones
        tournament = await tournament_repo.get(db, tournament_id)
        if not tournament or tournament.status != "registration_closed":
            raise ValueError("El torneo no está cerrado o no existe.")

        teams = await team_repo.get_approved_teams(db, tournament_id)
        if len(teams) < 2:
            raise ValueError("Se necesitan al menos 2 equipos para generar el bracket.")

        # 2. Cálculos iniciales
        num_teams = len(teams)
        power_of_2 = self.get_next_power_of_2(num_teams)
        num_byes = power_of_2 - num_teams
        total_rounds = int(math.log2(power_of_2))

        # Mezclar equipos
        random.shuffle(teams)

        # 3. Preparar lista de slots para la ronda 1
        # Llenaremos con Team y "BYE" (representado por None)
        slots = []
        # Distribuir equipos
        for t in teams:
            slots.append(t)
        # Distribuir BYEs
        for _ in range(num_byes):
            slots.append(None)
            
        # Mezclar nuevamente los slots para que los BYE no queden juntos necesariamente,
        # pero es mejor asegurarse de que no se enfrenten dos BYEs.
        # Mejor algoritmo: poner BYEs al final, y luego crear emparejamientos.
        # En eliminación directa estándar, los equipos principales van contra los peores.
        # Al ser aleatorio, simplemente repartimos.
        # Los slots emparejados son (slots[i], slots[i+1]). Para evitar BYE vs BYE (que no tiene sentido),
        # nos aseguramos de que no haya más BYEs que la mitad de la potencia de 2.
        # num_byes siempre será < power_of_2 / 2, así que si ponemos BYEs en índices impares, nunca chocarán.
        
        final_slots = [None] * power_of_2
        # Asignar BYEs
        bye_indices = random.sample(range(1, power_of_2, 2), num_byes)
        for i in bye_indices:
            final_slots[i] = "BYE"
            
        # Llenar el resto con equipos
        team_idx = 0
        for i in range(power_of_2):
            if final_slots[i] != "BYE":
                final_slots[i] = teams[team_idx]
                team_idx += 1

        # 4. Crear Rondas y Partidos en DB
        rounds_dict = {}
        for r_num in range(1, total_rounds + 1):
            r = await round_repo.create(db, obj_in={
                "tournament_id": tournament_id,
                "round_number": r_num,
                "name": self.get_round_name(r_num, total_rounds)
            })
            rounds_dict[r_num] = { "entity": r, "matches": [] }

        # 5. Generar estructura de partidos de Final hacia Ronda 1 para poder asignar next_match_id
        # Arreglo para guardar partidos por ronda
        # matches_by_round[r_num][match_index_in_round]
        matches_by_round = {}
        
        for r_num in range(total_rounds, 0, -1):
            matches_by_round[r_num] = []
            num_matches_in_round = 2 ** (total_rounds - r_num)
            for m_idx in range(num_matches_in_round):
                next_match_id = None
                if r_num < total_rounds:
                    # Encontrar partido padre
                    parent_match_idx = m_idx // 2
                    next_match_id = matches_by_round[r_num + 1][parent_match_idx].id
                
                match = await match_repo.create(db, obj_in={
                    "tournament_id": tournament_id,
                    "round_id": rounds_dict[r_num]["entity"].id,
                    "next_match_id": next_match_id
                })
                matches_by_round[r_num].append(match)
        
        # 6. Llenar los partidos de Ronda 1 con los equipos
        r1_matches = matches_by_round[1]
        for m_idx in range(len(r1_matches)):
            match = r1_matches[m_idx]
            t1 = final_slots[m_idx * 2]
            t2 = final_slots[m_idx * 2 + 1]
            
            update_data = {
                "team1_id": t1.id if t1 != "BYE" else None,
                "team2_id": t2.id if t2 != "BYE" else None
            }
            
            # Si hay un BYE, avanzar automáticamente al equipo válido
            if t1 == "BYE" or t2 == "BYE":
                winner = t2 if t1 == "BYE" else t1
                update_data["winner_team_id"] = winner.id
                update_data["status"] = "completed"
                update_data["score_team1"] = 0
                update_data["score_team2"] = 0
                # Tenemos que propagar este avance al siguiente partido
                await self._propagate_winner(db, match.id, winner.id, r1_matches)
            
            await match_repo.update(db, db_obj=match, obj_in=update_data)

        # 7. Actualizar el estado del torneo
        tournament.status = "bracket_generated"
        await db.commit()
        return True

    async def _propagate_winner(self, db: AsyncSession, current_match_id: str, winner_id: str, all_r1_matches: List[Match]):
        # Esta función es simplificada porque en la inicialización tenemos los objetos recién creados.
        # Mejor usar una query real al siguiente partido
        current_match = await match_repo.get(db, current_match_id)
        if current_match and current_match.next_match_id:
            next_m = await match_repo.get(db, current_match.next_match_id)
            # Determinar si el partido actual era el partido 1 o 2 que alimenta al siguiente
            # Para simplificar: el siguiente partido tiene team1_id y team2_id. 
            # Llenamos el que esté vacío.
            if next_m.team1_id is None:
                await match_repo.update(db, db_obj=next_m, obj_in={"team1_id": winner_id})
            elif next_m.team2_id is None:
                await match_repo.update(db, db_obj=next_m, obj_in={"team2_id": winner_id})

bracket_service = BracketService()
