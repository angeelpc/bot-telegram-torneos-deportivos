from aiogram import Router, Dispatcher
from .handlers import general_router, organizer_router, captain_router

def setup_routers(dp: Dispatcher):
    dp.include_router(general_router)
    dp.include_router(organizer_router)
    dp.include_router(captain_router)
