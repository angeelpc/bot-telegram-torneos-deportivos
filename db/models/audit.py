from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.database import Base
from db.models.base import generate_uuid, utc_now

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    tournament_id = Column(UUID(as_uuid=False), ForeignKey("tournaments.id"), nullable=False)
    message = Column(String, nullable=False)
    sent_at = Column(DateTime(timezone=True), default=utc_now)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=False), primary_key=True, default=generate_uuid)
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=utc_now)
