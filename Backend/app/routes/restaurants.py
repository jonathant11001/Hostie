import secrets
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import RestaurantProfile, APIKey, WeeklySchedule, Workspace
from ..dependencies import get_db
from ..schemas import (
    RestaurantProfileCreate,
    RestaurantProfileResponse,
    WeeklyScheduleCreate,
    WeeklyScheduleResponse
)

router = APIRouter(prefix="/workspaces", tags=["restaurants"])


@router.post("/{workspace_id}/restaurant", response_model=RestaurantProfileResponse)
def create_restaurant_profile(
    workspace_id: UUID,
    payload: RestaurantProfileCreate,
    db: Session = Depends(get_db)
):
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    restaurant_profile = RestaurantProfile(
        workspace_id=workspace_id,
        restaurant_name=payload.restaurant_name,
        cuisine_type=payload.cuisine_type,
        description=payload.description,
        address=payload.address,
        phone=payload.phone,
        email=payload.email
    )
    db.add(restaurant_profile)
    db.commit()
    db.refresh(restaurant_profile)

    return restaurant_profile

@router.post("/{workspace_id}/hours", response_model=WeeklyScheduleResponse)
def create_or_update_hours(
    workspace_id: UUID,
    payload: WeeklyScheduleCreate,
    db: Session = Depends(get_db)
):
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    # Prevent duplicate days (acts like upsert)
    existing = db.query(WeeklySchedule).filter(
        WeeklySchedule.workspace_id == workspace_id,
        WeeklySchedule.day_of_week == payload.day_of_week
    ).first()

    if existing:
        existing.open_time = payload.open_time
        existing.close_time = payload.close_time
        existing.is_closed = payload.is_closed
        db.commit()
        db.refresh(existing)
        return existing

    new_hours = WeeklySchedule(
        workspace_id=workspace_id,
        day_of_week=payload.day_of_week,
        open_time=payload.open_time,
        close_time=payload.close_time,
        is_closed=payload.is_closed
    )

    db.add(new_hours)
    db.commit()
    db.refresh(new_hours)

    return new_hours

@router.get("/{workspace_id}/hours", response_model=list[WeeklyScheduleResponse])
def get_restaurant_hours(
    workspace_id: UUID,
    db: Session = Depends(get_db)
):
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()

    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    hours = db.query(WeeklySchedule).filter(
        WeeklySchedule.workspace_id == workspace_id
    ).order_by(WeeklySchedule.day_of_week).all()

    return hours
