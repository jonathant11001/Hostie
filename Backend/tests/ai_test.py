from app.models.restaurant import RestaurantProfile
from app.models.weekly_schedule import WeeklySchedule
from app.services.context_builder import build_context
from app.services.chat_service import get_gemini_reply

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _format_schedule(schedules: list) -> str:
    lines = []
    for s in sorted(schedules, key=lambda x: x.day_of_week):
        day = DAY_NAMES[s.day_of_week]
        if s.is_closed:
            lines.append(f"{day}: Closed")
        else:
            lines.append(
                f"{day}: {s.open_time.strftime('%I:%M %p')} – {s.close_time.strftime('%I:%M %p')}"
            )
    return "\n".join(lines)


def test_ai_location_and_schedule(db):
    # Fetch existing data seeded by user_test2
    profile = db.query(RestaurantProfile).filter(
        RestaurantProfile.restaurant_name == "Maria's Bistro"
    ).first()
    assert profile is not None, "RestaurantProfile not found — run test_full_owner_workflow first"

    schedules = db.query(WeeklySchedule).filter(
        WeeklySchedule.workspace_id == profile.workspace_id
    ).all()
    assert len(schedules) == 7, f"Expected 7 schedule entries, found {len(schedules)}"

    # Build system prompt with restaurant info + schedule
    schedule_text = _format_schedule(schedules)
    system_prompt = build_context(profile) + f"\n\nWeekly Schedule:\n{schedule_text}"

    # Q1: Where is the restaurant?
    reply_location = get_gemini_reply(system_prompt, [], "Where is the restaurant?")
    print(f"\n[Location reply]\n{reply_location}")
    assert reply_location, "Expected a non-empty reply"
    assert "chicago" in reply_location.lower() or "olive" in reply_location.lower(), (
        f"Expected address in reply, got: {reply_location}"
    )

    # Q2: What is the weekly schedule?
    history = [
        {"role": "user",      "content": "Where is the restaurant?"},
        {"role": "assistant", "content": reply_location},
    ]
    reply_schedule = get_gemini_reply(system_prompt, history, "What is the weekly schedule?")
    print(f"\n[Schedule reply]\n{reply_schedule}")
    assert reply_schedule, "Expected a non-empty reply"
    assert "friday" in reply_schedule.lower() or "monday" in reply_schedule.lower(), (
        f"Expected schedule days in reply, got: {reply_schedule}"
    )
