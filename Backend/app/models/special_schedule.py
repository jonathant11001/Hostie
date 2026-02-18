import uuid
from sqlalchemy import Column, Date, Time, Boolean, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base


class SpecialSchedule(Base):
    __tablename__ = "special_schedule"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"))

    date = Column(Date, nullable=False)
    open_time = Column(Time)
    close_time = Column(Time)
    is_closed = Column(Boolean, default=False)
    reason = Column(Text)

    workspace = relationship("Workspace", back_populates="special_schedules")
