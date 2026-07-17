from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.base import generate_uuid

class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    tournament_id = Column(UUID(as_uuid=False), ForeignKey("tournaments.id"), nullable=False)
    name = Column(String, nullable=False) # e.g. "2011-2012", "Libre Femenil"
    
    tournament = relationship("Tournament", back_populates="categories")
    teams = relationship("Team", back_populates="category")
    rounds = relationship("Round", back_populates="category")
