"""Service layer for special schedule business logic."""

from uuid import UUID
from datetime import date, time
from sqlalchemy.orm import Session
from ..crud import special_schedule as special_crud


def add_special_schedule(db: Session, workspace_id: UUID, date_: date, open_time: time = None, close_time: time = None, is_closed: bool = False, reason: str = None):
    """Add a special schedule entry."""
    return special_crud.create_special_schedule(db, workspace_id, date_, open_time, close_time, is_closed, reason)
