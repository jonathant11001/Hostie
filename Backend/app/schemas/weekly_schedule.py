from pydantic import BaseModel, Field
from uuid import UUID
from datetime import time


class WeeklyScheduleBase(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    open_time: time | None = None
    close_time: time | None = None
    is_closed: bool = False


class WeeklyScheduleCreate(BaseModel):
    day_of_week: int
    open_time: time | None = None
    close_time: time | None = None
    is_closed: bool = False


class WeeklyScheduleResponse(WeeklyScheduleCreate):
    id: UUID
    restaurant_id: UUID

    model_config = {"from_attributes": True}
