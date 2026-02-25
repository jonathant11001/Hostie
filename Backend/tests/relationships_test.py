import pytest
from app.models.user import User
from app.models.workspace import Workspace
from app.models.restaurant import RestaurantProfile
from app.models.chat import Conversation, Message
from app.models.weekly_schedule import WeeklySchedule
from app.models.special_schedule import SpecialSchedule
from app.models.restaurant import APIKey

# Relationship test: User and Workspace

def test_user_workspace_relationship(db):
    user = User(displayname="Rel User", username="reluser", email="rel@user.com", passwordHash="pw")
    db.add(user)
    db.commit()
    workspace = Workspace(name="Rel WS", slug="rel-ws", owner_id=user.id)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    assert workspace.owner_id == user.id
    assert workspace.owner.id == user.id
    assert workspace in user.workspaces

# Relationship test: RestaurantProfile and Conversation

def test_restaurant_conversation_relationship(db):
    workspace = Workspace(name="RestRel WS", slug="restrel-ws")
    db.add(workspace)
    db.commit()
    restaurant = RestaurantProfile(restaurant_name="Rel Rest", workspace_id=workspace.id)
    db.add(restaurant)
    db.commit()
    conversation = Conversation(restaurant_id=restaurant.id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    assert conversation.restaurant_id == restaurant.id
    assert restaurant.conversation.id == conversation.id

# Relationship test: Conversation and Message

def test_conversation_message_relationship(db):
    workspace = Workspace(name="Msg WS", slug="msg-ws")
    db.add(workspace)
    db.commit()
    restaurant = RestaurantProfile(restaurant_name="Msg Rest", workspace_id=workspace.id)
    db.add(restaurant)
    db.commit()
    conversation = Conversation(restaurant_id=restaurant.id)
    db.add(conversation)
    db.commit()
    message = Message(conversation_id=conversation.id, restaurant_id=restaurant.id, role="system", content="Hi!")
    db.add(message)
    db.commit()
    db.refresh(message)
    assert message.conversation_id == conversation.id
    assert message in conversation.messages
