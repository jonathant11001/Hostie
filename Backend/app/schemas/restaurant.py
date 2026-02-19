from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class RestaurantProfileCreate(BaseModel):
    restaurant_name: str
    cuisine_type: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class RestaurantProfileResponse(BaseModel):
    id: UUID
    workspace_id: UUID
    restaurant_name: str
    cuisine_type: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True
