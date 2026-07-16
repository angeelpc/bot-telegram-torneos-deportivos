from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.base import generate_uuid, utc_now

class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    organizer_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    status = Column(String, default="draft", nullable=False) # draft, registration_open, registration_closed, bracket_generated, in_progress, completed, cancelled
    max_teams = Column(Integer, default=32, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    organizer = relationship("User")
    teams = relationship("Team", back_populates="tournament")
    rounds = relationship("Round", back_populates="tournament")
