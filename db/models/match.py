from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.base import generate_uuid, utc_now

class Round(Base):
    __tablename__ = "rounds"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    tournament_id = Column(UUID(as_uuid=False), ForeignKey("tournaments.id"), nullable=False)
    round_number = Column(Integer, nullable=False) # 1, 2, 3...
    name = Column(String, nullable=False) # Octavos, Cuartos, Semifinal, Final
    
    tournament = relationship("Tournament", back_populates="rounds")
    matches = relationship("Match", back_populates="round")

class Match(Base):
    __tablename__ = "matches"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    tournament_id = Column(UUID(as_uuid=False), ForeignKey("tournaments.id"), nullable=False)
    round_id = Column(UUID(as_uuid=False), ForeignKey("rounds.id"), nullable=False)
    
    team1_id = Column(UUID(as_uuid=False), ForeignKey("teams.id"), nullable=True) # Puede ser Null temporalmente
    team2_id = Column(UUID(as_uuid=False), ForeignKey("teams.id"), nullable=True) # Puede ser Null si es BYE o no se ha definido
    
    winner_team_id = Column(UUID(as_uuid=False), ForeignKey("teams.id"), nullable=True)
    next_match_id = Column(UUID(as_uuid=False), ForeignKey("matches.id"), nullable=True)
    
    status = Column(String, default="pending") # pending, scheduled, in_progress, completed, cancelled
    scheduled_time = Column(DateTime(timezone=True), nullable=True)
    location = Column(String, nullable=True)
    
    score_team1 = Column(Integer, nullable=True)
    score_team2 = Column(Integer, nullable=True)

    round = relationship("Round", back_populates="matches")
    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])
    winner = relationship("Team", foreign_keys=[winner_team_id])
    next_match = relationship("Match", remote_side=[id])
