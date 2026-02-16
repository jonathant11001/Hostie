import secrets
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import Restaurant, APIKey, RestaurantHours
from ..dependencies import get_db
from ..schemas import (
    RestaurantCreate,
    RestaurantResponse,
    RestaurantWithKey,
    RestaurantHoursCreate,
    RestaurantHoursResponse
)

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


@router.post("/", response_model=RestaurantWithKey)
def create_restaurant(
    payload: RestaurantCreate,
    db: Session = Depends(get_db)
):
    restaurant = Restaurant(name=payload.name)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)

    api_key_value = secrets.token_hex(32)

    api_key = APIKey(
        key=api_key_value,
        restaurant_id=restaurant.id
    )

    db.add(api_key)
    db.commit()

    return {
        "restaurant": restaurant,
        "api_key": api_key_value
    }

@router.post("/{restaurant_id}/hours", response_model=RestaurantHoursResponse)
def create_or_update_hours(
    restaurant_id: UUID,
    payload: RestaurantHoursCreate,
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Prevent duplicate days (acts like upsert)
    existing = db.query(RestaurantHours).filter(
        RestaurantHours.restaurant_id == restaurant_id,
        RestaurantHours.day_of_week == payload.day_of_week
    ).first()

    if existing:
        existing.open_time = payload.open_time
        existing.close_time = payload.close_time
        existing.is_closed = payload.is_closed
        db.commit()
        db.refresh(existing)
        return existing

    new_hours = RestaurantHours(
        restaurant_id=restaurant_id,
        day_of_week=payload.day_of_week,
        open_time=payload.open_time,
        close_time=payload.close_time,
        is_closed=payload.is_closed
    )

    db.add(new_hours)
    db.commit()
    db.refresh(new_hours)

    return new_hours

@router.get("/{restaurant_id}/hours", response_model=list[RestaurantHoursResponse])
def get_restaurant_hours(
    restaurant_id: UUID,
    db: Session = Depends(get_db)
):
    restaurant = db.query(Restaurant).filter(
        Restaurant.id == restaurant_id
    ).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    hours = db.query(RestaurantHours).filter(
        RestaurantHours.restaurant_id == restaurant_id
    ).order_by(RestaurantHours.day_of_week).all()

    return hours
