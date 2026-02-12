from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


# ---------- Restaurant ----------

class RestaurantCreate(BaseModel):
    name: str


class RestaurantResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class RestaurantWithKey(BaseModel):
    restaurant: RestaurantResponse
    api_key: str


# ---------- Chat ----------

class ChatRequest(BaseModel):
    message: str
    conversation_id: UUID | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID