import uuid
from datetime import datetime, UTC
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..database import Base


class RestaurantProfile(Base):
    __tablename__ = "restaurant_profile"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"), unique=True)

    restaurant_name = Column(String, nullable=False)
    cuisine_type = Column(String)
    description = Column(Text)
    address = Column(Text)
    phone = Column(String)
    email = Column(String)

    # Relationships
    workspace = relationship("Workspace", back_populates="restaurant_profile")
    conversation = relationship("Conversation", back_populates="restaurant", uselist=False)


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String, unique=True, nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspace.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    workspace = relationship("Workspace", back_populates="api_keys")
