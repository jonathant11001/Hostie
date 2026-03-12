from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..models import Conversation, Message, APIKey
from ..models.restaurant import RestaurantProfile
from ..models.weekly_schedule import WeeklySchedule
from ..schemas import ChatRequest, ChatResponse
from ..dependencies import get_db, get_current_restaurant
from ..services.context_builder import build_context
from ..services.chat_service import get_gemini_reply
from ..crud.workspace import get_workspace_by_slug
from ..crud.restaurant import get_restaurant_profile_by_workspace

_DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _format_schedule(schedules) -> str:
    lines = []
    for s in sorted(schedules, key=lambda x: x.day_of_week):
        day = _DAY_NAMES[s.day_of_week]
        if s.is_closed:
            lines.append(f"{day}: Closed")
        else:
            lines.append(f"{day}: {s.open_time.strftime('%I:%M %p')} – {s.close_time.strftime('%I:%M %p')}")
    return "\n".join(lines)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/public/{workspace_slug}", response_model=ChatResponse)
def public_chat(workspace_slug: str, payload: ChatRequest, db: Session = Depends(get_db)):
    """Public chat endpoint — identified by workspace slug, no API key required."""
    workspace = get_workspace_by_slug(db, workspace_slug)
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")

    restaurant = get_restaurant_profile_by_workspace(db, workspace.id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant profile not found")

    # Get or create conversation
    if payload.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == payload.conversation_id,
            Conversation.restaurant_id == restaurant.id
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(restaurant_id=restaurant.id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    system_prompt = build_context(restaurant)

    schedules = db.query(WeeklySchedule).filter(
        WeeklySchedule.workspace_id == workspace.id
    ).all()
    if schedules:
        system_prompt += f"\n\nWeekly Schedule:\n{_format_schedule(schedules)}"

    # Load prior history before saving new user message
    history = [
        {"role": m.role, "content": m.content}
        for m in db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
            .all()
    ]

    db.add(Message(
        conversation_id=conversation.id,
        restaurant_id=restaurant.id,
        role="user",
        content=payload.message,
    ))
    db.commit()

    reply = get_gemini_reply(system_prompt, history, payload.message)

    db.add(Message(
        conversation_id=conversation.id,
        restaurant_id=restaurant.id,
        role="assistant",
        content=reply,
    ))
    db.commit()

    return {"response": reply, "conversation_id": conversation.id}


@router.post("/widget", response_model=ChatResponse)
def widget_chat(
    payload: ChatRequest,
    x_api_key: str = Header(...),
    db: Session = Depends(get_db),
):
    """Widget chat endpoint — identified by API key in X-Api-Key header."""
    api_key = db.query(APIKey).filter(APIKey.key == x_api_key).first()
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    restaurant = get_restaurant_profile_by_workspace(db, api_key.workspace_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant profile not found")

    if payload.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == payload.conversation_id,
            Conversation.restaurant_id == restaurant.id,
        ).first()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(restaurant_id=restaurant.id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    system_prompt = build_context(restaurant)

    schedules = db.query(WeeklySchedule).filter(
        WeeklySchedule.workspace_id == api_key.workspace_id
    ).all()
    if schedules:
        system_prompt += f"\n\nWeekly Schedule:\n{_format_schedule(schedules)}"

    history = [
        {"role": m.role, "content": m.content}
        for m in db.query(Message)
            .filter(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
            .all()
    ]

    db.add(Message(
        conversation_id=conversation.id,
        restaurant_id=restaurant.id,
        role="user",
        content=payload.message,
    ))
    db.commit()

    reply = get_gemini_reply(system_prompt, history, payload.message)

    db.add(Message(
        conversation_id=conversation.id,
        restaurant_id=restaurant.id,
        role="assistant",
        content=reply,
    ))
    db.commit()

    return {"response": reply, "conversation_id": conversation.id}


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