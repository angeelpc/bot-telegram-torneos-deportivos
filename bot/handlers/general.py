from aiogram import Router, types
from aiogram.filters import CommandStart, Command

general_router = Router()

@general_router.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(
        "👋 ¡Hola! Soy el bot organizador de torneos deportivos.\n\n"
        "Puedes usar los siguientes comandos:\n"
        "/crear_torneo - Crea un nuevo torneo\n"
        "/mis_torneos - Ver tus torneos\n"
        "/ayuda - Ver la lista completa de comandos"
    )

@general_router.message(Command("ayuda"))
async def help_command(message: types.Message):
    await message.answer(
        "📖 <b>Lista de comandos:</b>\n\n"
        "<b>Para organizadores:</b>\n"
        "/crear_torneo - Crear un torneo\n"
        "/mis_torneos - Administrar tus torneos\n\n"
        "<b>Para capitanes:</b>\n"
        "<i>Usa el enlace de invitación para registrar un equipo.</i>\n"
        "/mis_equipos - Ver tus equipos\n"
        "/partidos - Ver próximos partidos\n"
        "/bracket - Ver el bracket del torneo"
    )
