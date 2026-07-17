from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_organizer_menu(tournament_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👥 Equipos Registrados", callback_data=f"org_teams_{tournament_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🔒 Cerrar Registro", callback_data=f"org_close_{tournament_id}"),
        InlineKeyboardButton(text="🌳 Generar Bracket", callback_data=f"org_bracket_{tournament_id}")
    )
    builder.row(
        InlineKeyboardButton(text="🏆 Ingresar Resultado", callback_data=f"org_result_{tournament_id}"),
        InlineKeyboardButton(text="📢 Enviar Comunicado", callback_data=f"org_announce_{tournament_id}")
    )
    return builder.as_markup()

def get_categories_keyboard(categories: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=f"📁 {cat.name}", callback_data=f"join_cat_{cat.id}")
    builder.adjust(1)
    return builder.as_markup()

def get_join_tournament_keyboard(tournament_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✍️ Registrar mi Equipo", callback_data=f"join_{tournament_id}")
    return builder.as_markup()

def get_team_approval_keyboard(team_id: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Aprobar", callback_data=f"approve_{team_id}")
    builder.button(text="❌ Rechazar", callback_data=f"reject_{team_id}")
    return builder.as_markup()
