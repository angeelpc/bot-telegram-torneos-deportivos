from aiogram.fsm.state import State, StatesGroup

class TournamentCreateStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_categories = State()

class TeamRegisterStates(StatesGroup):
    waiting_for_team_name = State()

class MatchResultStates(StatesGroup):
    waiting_for_score_t1 = State()
    waiting_for_score_t2 = State()
