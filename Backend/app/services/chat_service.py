"""Service layer for chat-related business logic (conversations and messages)."""

from uuid import UUID
from sqlalchemy.orm import Session
from ..crud import chat as chat_crud
from ..crud.workspace import get_workspace_by_id


def start_conversation(db: Session, workspace_id: UUID):
    """Start a new conversation, ensuring it belongs to a workspace."""
    workspace = get_workspace_by_id(db, workspace_id)
    if not workspace:
        raise ValueError("Conversations must belong to a valid workspace.")
    return chat_crud.create_conversation(db, workspace_id)


def add_message(db: Session, conversation_id: UUID, workspace_id: UUID, role: str, content: str):
    """Add a message to a conversation."""
    return chat_crud.create_message(db, conversation_id, workspace_id, role, content)
