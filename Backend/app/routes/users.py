import hashlib
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models import User
from ..dependencies import get_db
from ..schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


def hash_password(password: str) -> str:
    """Simple password hashing using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    """Create a new user."""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == payload.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == payload.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    # Create new user with hashed password
    user = User(
        displayname=payload.displayname,
        username=payload.username,
        email=payload.email,
        passwordHash=hash_password(payload.password),
        role="owner"
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a user by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: Session = Depends(get_db)
):
    """List all users."""
    users = db.query(User).all()
    return users


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    """Update a user."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if new username is already taken (and different from current)
    if payload.username != user.username:
        existing_user = db.query(User).filter(User.username == payload.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
    
    # Check if new email is already taken (and different from current)
    if payload.email != user.email:
        existing_email = db.query(User).filter(User.email == payload.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
    
    user.displayname = payload.displayname
    user.username = payload.username
    user.email = payload.email
    user.passwordHash = hash_password(payload.password)
    
    db.commit()
    db.refresh(user)
    
    return user
