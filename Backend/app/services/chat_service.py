"""Service layer for chat-related business logic (conversations and messages)."""

from uuid import UUID
from sqlalchemy.orm import Session
from ..crud import chat as chat_crud


def start_conversation(db: Session, workspace_id: UUID):
    """Start a new conversation."""
    return chat_crud.create_conversation(db, workspace_id)


def add_message(db: Session, conversation_id: UUID, workspace_id: UUID, role: str, content: str):
    """Add a message to a conversation."""
    return chat_crud.create_message(db, conversation_id, workspace_id, role, content)
