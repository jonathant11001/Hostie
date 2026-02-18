from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List


class WorkspaceCreate(BaseModel):
    name: str
    slug: str
    owner_id: UUID


class WorkspaceResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    owner_id: UUID
    subscription_tier: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
