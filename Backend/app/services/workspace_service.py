"""Service layer for workspace-related business logic."""

from uuid import UUID
from sqlalchemy.orm import Session
from ..crud import workspace as workspace_crud
from ..crud.restaurant import get_restaurant_profile_by_workspace


def validate_guid(value) -> UUID | None:
    """Validate that the value is a valid UUID (Guid). Returns UUID or None."""
    try:
        return UUID(str(value))
    except (ValueError, TypeError):
        return None


def create_workspace(db: Session, name: str, slug: str, owner_id: UUID, subscription_tier: str = "free"):
    """Create a workspace (add business logic as needed)."""
    workspace = workspace_crud.create_workspace(db, name, slug, owner_id, subscription_tier)
    # Enforce: One workspace must have at least one restaurant
    restaurant = get_restaurant_profile_by_workspace(db, workspace.id)
    if not restaurant:
        raise ValueError("A workspace must have at least one restaurant. Please create a restaurant profile for this workspace.")
    return workspace


def get_workspace(db: Session, workspace_id: UUID, owner_id: UUID):
    """Get workspace by ID only if it belongs to the given owner. Validates workspace_id as UUID."""
    workspace_uuid = validate_guid(workspace_id)
    owner_uuid = validate_guid(owner_id)
    if not workspace_uuid or not owner_uuid:
        return None
    workspace = workspace_crud.get_workspace_by_id(db, workspace_uuid)
    if workspace and workspace.owner_id == owner_uuid:
        return workspace
    return None
