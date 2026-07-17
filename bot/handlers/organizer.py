from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states.states import TournamentCreateStates
from bot.keyboards.inline import get_organizer_menu
from db.database import AsyncSessionLocal
from services.tournament_service import tournament_service
from services.bracket_service import bracket_service
from db.repositories.tournament_repo import tournament_repo
from core.config import settings

organizer_router = Router()

@organizer_router.message(Command("crear_torneo"))
async def cmd_crear_torneo(message: types.Message, state: FSMContext):
    await message.answer("🏆 Ingresa el nombre de tu torneo:")
    await state.set_state(TournamentCreateStates.waiting_for_name)

@organizer_router.message(TournamentCreateStates.waiting_for_name)
async def process_tournament_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📝 Ingresa una breve descripción del torneo:")
    await state.set_state(TournamentCreateStates.waiting_for_description)

@organizer_router.message(TournamentCreateStates.waiting_for_description)
async def process_tournament_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    description = message.text
    
    async with AsyncSessionLocal() as db:
        tournament = await tournament_service.create_tournament(db, name, description, message.from_user.id)
        
    await state.clear()
    
    # Generar enlace de invitación de ejemplo (Deep linking)
    join_link = f"https://t.me/{(await message.bot.get_me()).username}?start=join_{tournament.id}"
    
    await message.answer(
        f"✅ <b>Torneo Creado Exitosamente</b>\n\n"
        f"<b>Nombre:</b> {name}\n"
        f"<b>Descripción:</b> {description}\n\n"
        f"Para que los equipos se registren, comparte este enlace:\n{join_link}",
        reply_markup=get_organizer_menu(tournament.id)
    )

@organizer_router.message(Command("mis_torneos"))
async def cmd_mis_torneos(message: types.Message):
    async with AsyncSessionLocal() as db:
        from db.repositories.user_repo import user_repo
        user = await user_repo.get_by_telegram_id(db, message.from_user.id)
        if not user:
            await message.answer("No tienes torneos registrados.")
            return
            
        tournaments = await tournament_repo.get_by_organizer(db, user.id)
        if not tournaments:
            await message.answer("No tienes torneos registrados.")
            return
            
        for t in tournaments:
            await message.answer(
                f"🏆 <b>{t.name}</b>\nEstado: {t.status}",
                reply_markup=get_organizer_menu(t.id)
            )

@organizer_router.callback_query(lambda c: c.data and c.data.startswith('org_close_'))
async def process_close_registration(callback_query: types.CallbackQuery):
    tournament_id = callback_query.data.split('_')[2]
    async with AsyncSessionLocal() as db:
        try:
            await tournament_service.close_registration(db, tournament_id)
            await callback_query.answer("Registro cerrado exitosamente.")
            await callback_query.message.answer("🔒 El registro de equipos ha sido cerrado. Ya puedes generar el bracket.")
        except Exception as e:
            await callback_query.answer(str(e), show_alert=True)

@organizer_router.callback_query(lambda c: c.data and c.data.startswith('org_bracket_'))
async def process_generate_bracket(callback_query: types.CallbackQuery):
    tournament_id = callback_query.data.split('_')[2]
    async with AsyncSessionLocal() as db:
        try:
            success = await bracket_service.generate_bracket(db, tournament_id)
            if success:
                await callback_query.answer("Bracket generado exitosamente.")
                await callback_query.message.answer("🌳 ¡Bracket generado! Usa /bracket para verlo y /partidos para administrar los encuentros.")
        except ValueError as e:
            await callback_query.answer(str(e), show_alert=True)
        except Exception as e:
            await callback_query.answer("Ocurrió un error inesperado al generar el bracket.", show_alert=True)

@organizer_router.callback_query(lambda c: c.data and c.data.startswith('org_'))
async def process_unimplemented_features(callback_query: types.CallbackQuery):
    # Catch-all for buttons that don't have logic yet
    await callback_query.answer("🛠️ ¡Esta función está en desarrollo! Pronto estará disponible.", show_alert=True)
