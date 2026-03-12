"""CRUD operations module for database models."""

from .user import *
from .restaurant import *
from .workspace import *
from .chat import *
from .weekly_schedule import *
from .special_schedule import *

__all__ = [
    # User CRUD
    "create_user",
    "get_user_by_id",
    "get_user_by_username",
    "get_user_by_email",
    "get_all_users",
    "update_user",
    "delete_user",
    # Restaurant CRUD
    "create_restaurant_profile",
    "get_restaurant_profile_by_id",
    "get_restaurant_profile_by_workspace",
    "update_restaurant_profile",
    "delete_restaurant_profile",
    # Workspace CRUD
    "create_workspace",
    "get_workspace_by_id",
    "get_workspace_by_slug",
    "get_user_workspaces",
    "update_workspace",
    "delete_workspace",
    # Chat CRUD
    "create_conversation",
    "get_conversation_by_id",
    "get_workspace_conversations",
    "delete_conversation",
    "create_message",
    "get_message_by_id",
    "get_conversation_messages",
    "delete_message",
    # Schedule CRUD
    "create_weekly_schedule",
    "get_weekly_schedule_by_id",
    "get_workspace_weekly_schedules",
    "update_weekly_schedule",
    "delete_weekly_schedule",
    "create_special_schedule",
    "get_special_schedule_by_id",
    "get_workspace_special_schedules",
    "update_special_schedule",
    "delete_special_schedule",
]
