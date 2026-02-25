"""Service layer for weekly schedule business logic."""

from uuid import UUID
from datetime import time
from sqlalchemy.orm import Session
from ..crud import weekly_schedule as weekly_crud


def add_weekly_schedule(db: Session, workspace_id: UUID, day_of_week: int, open_time: time = None, close_time: time = None, is_closed: bool = False):
    """Add a weekly schedule entry."""
    return weekly_crud.create_weekly_schedule(db, workspace_id, day_of_week, open_time, close_time, is_closed)
