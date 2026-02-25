"""Service layer for restaurant profile business logic."""

from uuid import UUID
from sqlalchemy.orm import Session
from ..crud import restaurant as restaurant_crud
from ..schemas.restaurant import RestaurantProfileCreate


def create_restaurant(db: Session, workspace_id: UUID, data: RestaurantProfileCreate):

    """Create a restaurant profile (add business logic as needed)."""
    return restaurant_crud.create_restaurant_profile(db, workspace_id, data)


def get_restaurant_profile(db: Session, restaurant_id: UUID):
    """Get restaurant profile by ID."""
    return restaurant_crud.get_restaurant_profile_by_id(db, restaurant_id)
