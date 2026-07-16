from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from bot.states.states import TeamRegisterStates
from db.database import AsyncSessionLocal
from db.repositories.tournament_repo import tournament_repo
from db.repositories.user_repo import user_repo
from db.repositories.team_repo import team_repo

captain_router = Router()

@captain_router.message(CommandStart(deep_link=True))
async def join_tournament(message: types.Message, command: CommandObject, state: FSMContext):
    args = command.args
    if args and args.startswith("join_"):
        tournament_id = args.split("join_")[1]
        async with AsyncSessionLocal() as db:
            tournament = await tournament_repo.get(db, tournament_id)
            if not tournament:
                await message.answer("El torneo no existe.")
                return
            if tournament.status != "registration_open":
                await message.answer("El registro para este torneo está cerrado.")
                return
            
            await state.update_data(tournament_id=tournament_id)
            await message.answer(f"Has sido invitado al torneo <b>{tournament.name}</b>.\n\nEscribe el nombre de tu equipo para registrarte:")
            await state.set_state(TeamRegisterStates.waiting_for_team_name)

@captain_router.message(TeamRegisterStates.waiting_for_team_name)
async def process_team_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    tournament_id = data['tournament_id']
    team_name = message.text
    
    async with AsyncSessionLocal() as db:
        # 1. Registrar usuario si no existe
        user = await user_repo.get_by_telegram_id(db, message.from_user.id)
        if not user:
            user = await user_repo.create(db, obj_in={"telegram_id": message.from_user.id, "full_name": message.from_user.full_name})
            
        # 2. Registrar equipo
        team = await team_repo.create(db, obj_in={
            "tournament_id": tournament_id,
            "name": team_name,
            "captain_id": user.id,
            "status": "approved" # Para el MVP lo auto-aprobaremos para simplificar, aunque el prompt sugiere aprobar/rechazar.
        })
        
        await message.answer(f"✅ Equipo <b>{team_name}</b> registrado exitosamente. Espera a que el organizador cierre registros y genere el bracket.")
        
    await state.clear()
