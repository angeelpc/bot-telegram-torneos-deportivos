from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    tournament_id: str
    captain_id: str

class TeamResponse(TeamBase):
    id: str
    tournament_id: str
    captain_id: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
