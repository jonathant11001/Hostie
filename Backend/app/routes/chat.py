from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import Conversation, Message
from ..models.restaurant import RestaurantProfile
from ..schemas import ChatRequest, ChatResponse
from ..dependencies import get_db, get_current_restaurant
from ..services.context_builder import build_context
from ..services.chat_service import get_gemini_reply

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    restaurant_id=Depends(get_current_restaurant),
    db: Session = Depends(get_db)
):
    # Get or create conversation
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

    # Build system prompt from restaurant profile
    restaurant = db.query(RestaurantProfile).filter(
        RestaurantProfile.id == restaurant_id
    ).first()
    system_prompt = build_context(restaurant) if restaurant else "You are a helpful restaurant assistant."

    # Load prior conversation history before saving the new user message
    history = [
        {"role": m.role, "content": m.content}
        for m in db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
            .all()
    ]

    # Persist user message
    db.add(Message(
        conversation_id=conversation.id,
        restaurant_id=restaurant_id,
        role="user",
        content=payload.message,
    ))
    db.commit()

    # Call Gemini
    reply = get_gemini_reply(system_prompt, history, payload.message)

    # Persist assistant reply
    db.add(Message(
        conversation_id=conversation.id,
        restaurant_id=restaurant_id,
        role="assistant",
        content=reply,
    ))
    db.commit()

    return {
        "response": reply,
        "conversation_id": conversation.id,
    }