"""CRUD operations for RestaurantProfile model."""

from uuid import UUID
from sqlalchemy.orm import Session
from ..models.restaurant import RestaurantProfile
from ..schemas.restaurant import RestaurantProfileCreate


def create_restaurant_profile(
    db: Session, workspace_id: UUID, restaurant: RestaurantProfileCreate
) -> RestaurantProfile:
    """Create a new restaurant profile.
    
    Args:
        db: Database session
        workspace_id: Workspace UUID
        restaurant: Restaurant profile creation schema
        
    Returns:
        Created RestaurantProfile object
    """
    db_restaurant = RestaurantProfile(
        workspace_id=workspace_id,
        restaurant_name=restaurant.restaurant_name,
        cuisine_type=restaurant.cuisine_type,
        description=restaurant.description,
        address=restaurant.address,
        phone=restaurant.phone,
        email=restaurant.email,
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def get_restaurant_profile_by_id(
    db: Session, restaurant_id: UUID
) -> RestaurantProfile | None:
    """Retrieve a restaurant profile by ID.
    
    Args:
        db: Database session
        restaurant_id: Restaurant profile UUID
        
    Returns:
        RestaurantProfile object or None if not found
    """
    return db.query(RestaurantProfile).filter(
        RestaurantProfile.id == restaurant_id
    ).first()


def get_restaurant_profile_by_workspace(
    db: Session, workspace_id: UUID
) -> RestaurantProfile | None:
    """Retrieve a restaurant profile by workspace ID.
    
    Args:
        db: Database session
        workspace_id: Workspace UUID
        
    Returns:
        RestaurantProfile object or None if not found
    """
    return db.query(RestaurantProfile).filter(
        RestaurantProfile.workspace_id == workspace_id
    ).first()


def update_restaurant_profile(
    db: Session, restaurant_id: UUID, restaurant_data: dict
) -> RestaurantProfile | None:
    """Update a restaurant profile.
    
    Args:
        db: Database session
        restaurant_id: Restaurant profile UUID
        restaurant_data: Dictionary of fields to update
        
    Returns:
        Updated RestaurantProfile object or None if not found
    """
    db_restaurant = get_restaurant_profile_by_id(db, restaurant_id)
    if not db_restaurant:
        return None
    
    for key, value in restaurant_data.items():
        if value is not None and hasattr(db_restaurant, key):
            setattr(db_restaurant, key, value)
    
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant


def delete_restaurant_profile(db: Session, restaurant_id: UUID) -> bool:
    """Delete a restaurant profile.
    
    Args:
        db: Database session
        restaurant_id: Restaurant profile UUID
        
    Returns:
        True if restaurant profile was deleted, False if not found
    """
    db_restaurant = get_restaurant_profile_by_id(db, restaurant_id)
    if not db_restaurant:
        return False
    
    db.delete(db_restaurant)
    db.commit()
    return True
