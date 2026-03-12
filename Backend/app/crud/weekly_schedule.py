"""CRUD operations for WeeklySchedule model."""

from uuid import UUID
from datetime import time
from sqlalchemy.orm import Session
from ..models.weekly_schedule import WeeklySchedule


def create_weekly_schedule(
    db: Session,
    workspace_id: UUID,
    day_of_week: int,
    open_time: time | None = None,
    close_time: time | None = None,
    is_closed: bool = False,
) -> WeeklySchedule:
    """Create a new weekly schedule entry."""
    db_schedule = WeeklySchedule(
        workspace_id=workspace_id,
        day_of_week=day_of_week,
        open_time=open_time,
        close_time=close_time,
        is_closed=is_closed,
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_weekly_schedule_by_id(
    db: Session, schedule_id: UUID
) -> WeeklySchedule | None:
    """Retrieve a weekly schedule entry by ID."""
    return db.query(WeeklySchedule).filter(
        WeeklySchedule.id == schedule_id
    ).first()


def get_workspace_weekly_schedules(
    db: Session, workspace_id: UUID
) -> list[WeeklySchedule]:
    """Retrieve all weekly schedules for a workspace."""
    return db.query(WeeklySchedule).filter(
        WeeklySchedule.workspace_id == workspace_id
    ).all()


def get_weekly_schedule_by_day(
    db: Session, workspace_id: UUID, day_of_week: int
) -> WeeklySchedule | None:
    """Retrieve a weekly schedule entry by workspace and day of week."""
    return db.query(WeeklySchedule).filter(
        WeeklySchedule.workspace_id == workspace_id,
        WeeklySchedule.day_of_week == day_of_week,
    ).first()


def update_weekly_schedule(
    db: Session, schedule_id: UUID, schedule_data: dict
) -> WeeklySchedule | None:
    """Update a weekly schedule entry."""
    db_schedule = get_weekly_schedule_by_id(db, schedule_id)
    if not db_schedule:
        return None
    for key, value in schedule_data.items():
        if hasattr(db_schedule, key):
            setattr(db_schedule, key, value)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def delete_weekly_schedule(db: Session, schedule_id: UUID) -> bool:
    """Delete a weekly schedule entry."""
    db_schedule = get_weekly_schedule_by_id(db, schedule_id)
    if not db_schedule:
        return False
    db.delete(db_schedule)
    db.commit()
    return True
