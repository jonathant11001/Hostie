from pydantic import BaseModel
from uuid import UUID
from datetime import date, time


class SpecialScheduleBase(BaseModel):
    date: date
    open_time: time | None = None
    close_time: time | None = None
    is_closed: bool = False
    reason: str | None = None


class SpecialScheduleCreate(SpecialScheduleBase):
    workspace_id: UUID


class SpecialScheduleResponse(SpecialScheduleBase):
    id: UUID
    workspace_id: UUID

    model_config = {"from_attributes": True}
