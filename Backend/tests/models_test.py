from app.models.user import User
from app.models.workspace import Workspace
from app.models.restaurant import RestaurantProfile
from app.models.chat import Conversation, Message
from app.models.weekly_schedule import WeeklySchedule
from app.models.special_schedule import SpecialSchedule
from app.models.restaurant import APIKey
import pytest
import datetime

# Assume a fixture 'db' provides a SQLAlchemy session

def test_create_workspace(db):
    workspace = Workspace(name="Test Workspace", slug="test-workspace")
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    assert workspace.id is not None
    assert workspace.name == "Test Workspace"

def test_create_restaurant_profile(db):
    workspace = Workspace(name="Rest WS", slug="rest-ws")
    db.add(workspace)
    db.commit()
    restaurant = RestaurantProfile(restaurant_name="Pizza Place", workspace_id=workspace.id)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    assert restaurant.id is not None
    assert restaurant.restaurant_name == "Pizza Place"
    assert restaurant.workspace_id == workspace.id

def test_create_conversation_and_message(db):
    workspace = Workspace(name="Chat WS", slug="chat-ws")
    db.add(workspace)
    db.commit()
    restaurant = RestaurantProfile(restaurant_name="Chat Rest", workspace_id=workspace.id)
    db.add(restaurant)
    db.commit()
    conversation = Conversation(restaurant_id=restaurant.id)
    db.add(conversation)
    db.commit()
    message = Message(conversation_id=conversation.id, restaurant_id=restaurant.id, role="user", content="Hello!")
    db.add(message)
    db.commit()
    db.refresh(message)
    assert message.id is not None
    assert message.role == "user"
    assert message.conversation_id == conversation.id

def test_create_weekly_schedule(db):
    workspace = Workspace(name="WS", slug="ws")
    db.add(workspace)
    db.commit()
    schedule = WeeklySchedule(
        workspace_id=workspace.id,
        day_of_week=0,  # 0 = Monday
        open_time=datetime.time(9, 0),
        close_time=datetime.time(17, 0)
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    assert schedule.id is not None
    assert schedule.day_of_week == 0

def test_create_special_schedule(db):
    workspace = Workspace(name="WS2", slug="ws2")
    db.add(workspace)
    db.commit()
    schedule = SpecialSchedule(
        workspace_id=workspace.id,
        date=datetime.date(2026, 2, 24),
        open_time=datetime.time(10, 0),
        close_time=datetime.time(15, 0)
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    assert schedule.id is not None
    assert schedule.date == datetime.date(2026, 2, 24)

def test_create_apikey(db):
    workspace = Workspace(name="API WS", slug="api-ws")
    db.add(workspace)
    db.commit()
    apikey = APIKey(key="testkey123", workspace_id=workspace.id)
    db.add(apikey)
    db.commit()
    db.refresh(apikey)
    assert apikey.id is not None
    assert apikey.key == "testkey123"
