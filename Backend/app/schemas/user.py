from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    displayname: str
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    displayname: str
    username: str
    email: EmailStr
    role: str | None = None
    avatarUrl: str | None = None
    createdAt: datetime

    model_config = {"from_attributes": True}
