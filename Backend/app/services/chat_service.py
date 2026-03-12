from uuid import UUID
from sqlalchemy.orm import Session
from google import genai
from google.genai import types
from ..crud import chat as chat_crud
from ..crud.workspace import get_workspace_by_id
from ..config import settings


def start_conversation(db: Session, workspace_id: UUID):
    """Start a new conversation, ensuring it belongs to a workspace."""
    workspace = get_workspace_by_id(db, workspace_id)
    if not workspace:
        raise ValueError("Conversations must belong to a valid workspace.")
    return chat_crud.create_conversation(db, workspace_id)


def add_message(db: Session, conversation_id: UUID, workspace_id: UUID, role: str, content: str):
    """Add a message to a conversation."""
    return chat_crud.create_message(db, conversation_id, workspace_id, role, content)


def get_gemini_reply(system_prompt: str, history: list[dict], user_message: str) -> str:
    """Send a message to Gemini and return the reply, passing full conversation history."""
    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    contents = [
        types.Content(
            role="model" if m["role"] == "assistant" else "user",
            parts=[types.Part(text=m["content"])],
        )
        for m in history
    ]
    contents.append(types.Content(role="user", parts=[types.Part(text=user_message)]))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )
    return response.text
