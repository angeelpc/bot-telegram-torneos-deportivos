from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from .team import TeamResponse

class MatchBase(BaseModel):
    status: str
    scheduled_time: Optional[datetime] = None
    location: Optional[str] = None
    score_team1: Optional[int] = None
    score_team2: Optional[int] = None

class MatchResponse(MatchBase):
    id: str
    tournament_id: str
    round_id: str
    team1_id: Optional[str] = None
    team2_id: Optional[str] = None
    winner_team_id: Optional[str] = None
    next_match_id: Optional[str] = None

    team1: Optional[TeamResponse] = None
    team2: Optional[TeamResponse] = None

    model_config = ConfigDict(from_attributes=True)
