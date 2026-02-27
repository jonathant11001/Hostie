"""Service layer for user-related business logic."""

from uuid import UUID
from sqlalchemy.orm import Session
from ..crud import user as user_crud
from ..schemas.user import UserCreate
from passlib.context import CryptContext
from fastapi.exceptions import PermissionError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def check_user_role(user, required_role: str):
    if user.role != required_role:
        raise PermissionError(f"User must have role '{required_role}' to perform this action.")

def register_user(db: Session, user_data: UserCreate, password: str):
    """Register a new user (with business logic, e.g., email validation, etc)."""

    existing_user = user_crud.get_user_by_username(db, user_data.username)
    if existing_user:
        raise ValueError("Username already taken")
    existing_email = user_crud.get_user_by_email(db, user_data.email)
    if existing_email:
        raise ValueError("Email already taken")
    password_hash = hash_password(password)
    return user_crud.create_user(db, user_data, password_hash)

def get_user_profile(db: Session, user_id: UUID):
    """Get user profile by ID."""
    return user_crud.get_user_by_id(db, user_id)
