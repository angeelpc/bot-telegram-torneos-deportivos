from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.base import generate_uuid, utc_now

class Team(Base):
    __tablename__ = "teams"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    tournament_id = Column(UUID(as_uuid=False), ForeignKey("tournaments.id"), nullable=False)
    name = Column(String, nullable=False)
    captain_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    status = Column(String, default="pending", nullable=False) # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), default=utc_now)

    tournament = relationship("Tournament", back_populates="teams")
    captain = relationship("User")
    members = relationship("TeamMember", back_populates="team")

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    team_id = Column(UUID(as_uuid=False), ForeignKey("teams.id"), nullable=False)
    telegram_id = Column(BigInteger, nullable=False)
    name = Column(String, nullable=False)

    team = relationship("Team", back_populates="members")
