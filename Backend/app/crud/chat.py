"""CRUD operations for Chat models (Conversation and Message)."""

from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..app.models.chat import Conversation, Message


# ============================================================================
# CONVERSATION CRUD
# ============================================================================


def create_conversation(db: Session, workspace_id: UUID) -> Conversation:
    """Create a new conversation.
    
    Args:
        db: Database session
        workspace_id: Workspace UUID
        
    Returns:
        Created Conversation object
    """
    db_conversation = Conversation(
        restaurant_id=workspace_id,
        created_at=datetime.utcnow(),
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def get_conversation_by_id(db: Session, conversation_id: UUID) -> Conversation | None:
    """Retrieve a conversation by ID.
    
    Args:
        db: Database session
        conversation_id: Conversation UUID
        
    Returns:
        Conversation object or None if not found
    """
    return db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()


def get_workspace_conversations(
    db: Session, workspace_id: UUID, skip: int = 0, limit: int = 100
) -> list[Conversation]:
    """Retrieve all conversations in a workspace.
    
    Args:
        db: Database session
        workspace_id: Workspace UUID
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Conversation objects
    """
    return db.query(Conversation).filter(
        Conversation.restaurant_id == workspace_id
    ).offset(skip).limit(limit).all()


def delete_conversation(db: Session, conversation_id: UUID) -> bool:
    """Delete a conversation and all its messages.
    
    Args:
        db: Database session
        conversation_id: Conversation UUID
        
    Returns:
        True if conversation was deleted, False if not found
    """
    db_conversation = get_conversation_by_id(db, conversation_id)
    if not db_conversation:
        return False
    
    db.delete(db_conversation)
    db.commit()
    return True


# ============================================================================
# MESSAGE CRUD
# ============================================================================


def create_message(
    db: Session,
    conversation_id: UUID,
    workspace_id: UUID,
    role: str,
    content: str,
) -> Message:
    """Create a new message in a conversation.
    
    Args:
        db: Database session
        conversation_id: Conversation UUID
        workspace_id: Workspace UUID
        role: Message role (e.g., "user", "assistant", "system")
        content: Message content text
        
    Returns:
        Created Message object
    """
    db_message = Message(
        conversation_id=conversation_id,
        restaurant_id=workspace_id,
        role=role,
        content=content,
        created_at=datetime.utcnow(),
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_message_by_id(db: Session, message_id: UUID) -> Message | None:
    """Retrieve a message by ID.
    
    Args:
        db: Database session
        message_id: Message UUID
        
    Returns:
        Message object or None if not found
    """
    return db.query(Message).filter(Message.id == message_id).first()


def get_conversation_messages(
    db: Session, conversation_id: UUID, skip: int = 0, limit: int = 100
) -> list[Message]:
    """Retrieve all messages in a conversation.
    
    Args:
        db: Database session
        conversation_id: Conversation UUID
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of Message objects
    """
    return db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).offset(skip).limit(limit).all()


def delete_message(db: Session, message_id: UUID) -> bool:
    """Delete a message.
    
    Args:
        db: Database session
        message_id: Message UUID
        
    Returns:
        True if message was deleted, False if not found
    """
    db_message = get_message_by_id(db, message_id)
    if not db_message:
        return False
    
    db.delete(db_message)
    db.commit()
    return True
