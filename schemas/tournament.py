from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class TournamentBase(BaseModel):
    name: str
    description: Optional[str] = None
    max_teams: int = 32

class TournamentCreate(TournamentBase):
    organizer_id: str

class TournamentResponse(TournamentBase):
    id: str
    organizer_id: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
