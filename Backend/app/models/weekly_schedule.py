import uuid
from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base


class WeeklySchedule(Base):
    __tablename__ = "restaurant_hours"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), nullable=False)

    day_of_week = Column(Integer, nullable=False)  # 0 = Monday, 6 = Sunday
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    is_closed = Column(Boolean, default=False)

    workspace = relationship("Workspace", back_populates="weekly_schedules")
