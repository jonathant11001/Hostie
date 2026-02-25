"""CRUD operations for Workspace model."""

from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..app.models.workspace import Workspace


def create_workspace(
    db: Session, name: str, slug: str, owner_id: UUID, subscription_tier: str = "free"
) -> Workspace:
    """Create a new workspace.
    
    Args:
        db: Database session
        name: Workspace name
        slug: URL-friendly workspace identifier (must be unique)
        owner_id: Owner user UUID
        subscription_tier: Subscription level (default: "free")
        
    Returns:
        Created Workspace object
        
    Raises:
        IntegrityError: If slug already exists
    """
    db_workspace = Workspace(
        name=name,
        slug=slug,
        owner_id=owner_id,
        subscription_tier=subscription_tier,
    )
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    return db_workspace


def get_workspace_by_id(db: Session, workspace_id: UUID) -> Workspace | None:
    """Retrieve a workspace by ID.
    
    Args:
        db: Database session
        workspace_id: Workspace UUID
        
    Returns:
        Workspace object or None if not found
    """
    return db.query(Workspace).filter(Workspace.id == workspace_id).first()


def get_workspace_by_slug(db: Session, slug: str) -> Workspace | None:
    """Retrieve a workspace by slug.
    
    Args:
        db: Database session
        slug: Workspace slug
        
    Returns:
        Workspace object or None if not found
    """
    return db.query(Workspace).filter(Workspace.slug == slug).first()


def get_user_workspaces(db: Session, owner_id: UUID, skip: int = 0, limit: int = 100) -> list[Workspace]:
    """Retrieve all workspaces owned by a user.
    
    Args:
        db: Database session
        owner_id: Owner user UUID
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Workspace objects
    """
    return db.query(Workspace).filter(
        Workspace.owner_id == owner_id
    ).offset(skip).limit(limit).all()


def update_workspace(
    db: Session, workspace_id: UUID, workspace_data: dict
) -> Workspace | None:
    """Update a workspace.
    
    Args:
        db: Database session
        workspace_id: Workspace UUID
        workspace_data: Dictionary of fields to update
        
    Returns:
        Updated Workspace object or None if not found
    """
    db_workspace = get_workspace_by_id(db, workspace_id)
    if not db_workspace:
        return None
    
    for key, value in workspace_data.items():
        if value is not None and hasattr(db_workspace, key):
            setattr(db_workspace, key, value)
    
    db.commit()
    db.refresh(db_workspace)
    return db_workspace


def delete_workspace(db: Session, workspace_id: UUID) -> bool:
    """Delete a workspace.
    
    Args:
        db: Database session
        workspace_id: Workspace UUID
        
    Returns:
        True if workspace was deleted, False if not found
    """
    db_workspace = get_workspace_by_id(db, workspace_id)
    if not db_workspace:
        return False
    
    db.delete(db_workspace)
    db.commit()
    return True
