import uuid
from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    displayname = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    passwordHash = Column(Text, nullable=False)
    role = Column(String, default="owner")
    avatarUrl = Column(Text)
    createdAt = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    workspaces = relationship("Workspace", back_populates="owner")