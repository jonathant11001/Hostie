"""Service layer for user-related business logic."""

from uuid import UUID
from sqlalchemy.orm import Session
from ..crud import user as user_crud
from ..schemas.user import UserCreate


def register_user(db: Session, user_data: UserCreate, password_hash: str):
    """Register a new user (with business logic, e.g., email validation, etc)."""
    # Add business logic here (e.g., check for existing email, send welcome email)
    return user_crud.create_user(db, user_data, password_hash)


def get_user_profile(db: Session, user_id: UUID):
    """Get user profile by ID."""
    return user_crud.get_user_by_id(db, user_id)
