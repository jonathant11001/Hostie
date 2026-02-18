import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Workspace(Base):
    __tablename__ = "workspace"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    subscription_tier = Column(String, default="free")
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    owner = relationship("User", back_populates="workspaces")
    restaurant_profile = relationship("RestaurantProfile", back_populates="workspace", uselist=False)
    weekly_schedules = relationship("WeeklySchedule", back_populates="workspace")
    special_schedules = relationship("SpecialSchedule", back_populates="workspace")