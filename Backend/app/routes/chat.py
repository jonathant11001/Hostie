from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import Conversation, Message
from ..schemas import ChatRequest, ChatResponse
from ..dependencies import get_db, get_current_restaurant
import uuid

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    restaurant_id=Depends(get_current_restaurant),
    db: Session = Depends(get_db)
):
    # Create conversation if not provided
    if payload.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == payload.conversation_id,
            Conversation.restaurant_id == restaurant_id
        ).first()
    else:
        conversation = Conversation(restaurant_id=restaurant_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # Save user message
    user_message = Message(
        conversation_id=conversation.id,
        restaurant_id=restaurant_id,
        role="user",
        content=payload.message
    )
    db.add(user_message)

    # Mock assistant response
    assistant_response_text = "This is a mock response from Hostie."

    assistant_message = Message(
        conversation_id=conversation.id,
        restaurant_id=restaurant_id,
        role="assistant",
        content=assistant_response_text
    )
    db.add(assistant_message)

    db.commit()

    return {
        "response": assistant_response_text,
        "conversation_id": conversation.id
    }