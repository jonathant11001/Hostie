"""CRUD operations for User model."""

from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..app.models.user import User
from ..app.schemas.user import UserCreate


def create_user(db: Session, user: UserCreate, password_hash: str) -> User:
    """Create a new user in the database.
    
    Args:
        db: Database session
        user: User creation schema with displayname, username, email
        password_hash: Hashed password
        
    Returns:
        Created User object
        
    Raises:
        IntegrityError: If username or email already exists
    """
    db_user = User(
        displayname=user.displayname,
        username=user.username,
        email=user.email,
        passwordHash=password_hash,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: UUID) -> User | None:
    """Retrieve a user by ID.
    
    Args:
        db: Database session
        user_id: User UUID
        
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """Retrieve a user by username.
    
    Args:
        db: Database session
        username: User's username
        
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Retrieve a user by email.
    
    Args:
        db: Database session
        email: User's email address
        
    Returns:
        User object or None if not found
    """
    return db.query(User).filter(User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Retrieve all users with pagination.
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of User objects
    """
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: UUID, user_data: dict) -> User | None:
    """Update a user's information.
    
    Args:
        db: Database session
        user_id: User UUID
        user_data: Dictionary of fields to update
        
    Returns:
        Updated User object or None if not found
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    for key, value in user_data.items():
        if value is not None and hasattr(db_user, key):
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: UUID) -> bool:
    """Delete a user from the database.
    
    Args:
        db: Database session
        user_id: User UUID
        
    Returns:
        True if user was deleted, False if not found
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True
