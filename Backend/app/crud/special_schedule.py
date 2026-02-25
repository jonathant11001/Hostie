"""CRUD operations for SpecialSchedule model."""

from uuid import UUID
from datetime import date, time
from sqlalchemy.orm import Session
from ..app.models.special_schedule import SpecialSchedule


def create_special_schedule(
    db: Session,
    workspace_id: UUID,
    date: date,
    open_time: time | None = None,
    close_time: time | None = None,
    is_closed: bool = False,
    reason: str | None = None,
) -> SpecialSchedule:
    """Create a new special schedule entry."""
    db_schedule = SpecialSchedule(
        workspace_id=workspace_id,
        date=date,
        open_time=open_time,
        close_time=close_time,
        is_closed=is_closed,
        reason=reason,
    )
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_special_schedule_by_id(
    db: Session, schedule_id: UUID
) -> SpecialSchedule | None:
    """Retrieve a special schedule entry by ID."""
    return db.query(SpecialSchedule).filter(
        SpecialSchedule.id == schedule_id
    ).first()


def get_workspace_special_schedules(
    db: Session, workspace_id: UUID, skip: int = 0, limit: int = 100
) -> list[SpecialSchedule]:
    """Retrieve all special schedules for a workspace."""
    return db.query(SpecialSchedule).filter(
        SpecialSchedule.workspace_id == workspace_id
    ).offset(skip).limit(limit).all()


def get_special_schedule_by_date(
    db: Session, workspace_id: UUID, date: date
) -> SpecialSchedule | None:
    """Retrieve a special schedule entry by workspace and date."""
    return db.query(SpecialSchedule).filter(
        SpecialSchedule.workspace_id == workspace_id,
        SpecialSchedule.date == date,
    ).first()


def update_special_schedule(
    db: Session, schedule_id: UUID, schedule_data: dict
) -> SpecialSchedule | None:
    """Update a special schedule entry."""
    db_schedule = get_special_schedule_by_id(db, schedule_id)
    if not db_schedule:
        return None
    for key, value in schedule_data.items():
        if hasattr(db_schedule, key):
            setattr(db_schedule, key, value)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def delete_special_schedule(db: Session, schedule_id: UUID) -> bool:
    """Delete a special schedule entry."""
    db_schedule = get_special_schedule_by_id(db, schedule_id)
    if not db_schedule:
        return False
    db.delete(db_schedule)
    db.commit()
    return True
