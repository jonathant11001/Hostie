from pydantic import BaseModel
from uuid import UUID
from typing import List
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    conversation_id: UUID | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: UUID


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    restaurant_id: UUID | None = None
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: UUID
    restaurant_id: UUID | None = None
    created_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True
