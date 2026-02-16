from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime, time


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

class RestaurantWithKey(BaseModel):
    restaurant: RestaurantResponse
    api_key: str


# ---------- Restaurant Hours ----------

class RestaurantHoursBase(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    open_time: time | None = None
    close_time: time | None = None
    is_closed: bool = False


class RestaurantHoursCreate(BaseModel):
    day_of_week: int
    open_time: time | None = None
    close_time: time | None = None
    is_closed: bool = False


class RestaurantHoursResponse(RestaurantHoursCreate):
    id: UUID
    restaurant_id: UUID

    class Config:
        from_attributes = True

# ---------- Chat ----------

class ChatRequest(BaseModel):
    message: str
    conversation_id: UUID | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID