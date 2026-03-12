from datetime import time
from app.models.user import User
from app.models.workspace import Workspace
from app.models.restaurant import RestaurantProfile
from app.models.weekly_schedule import WeeklySchedule


def test_full_owner_workflow(db):
    # 1. Create user
    user = User(
        displayname="Maria",
        username="maria_bistro",
        email="maria@bistro.com",
        passwordHash="hashed_pw",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.role == "owner"
    assert user.createdAt is not None

    # 2. Create workspace owned by the user
    workspace = Workspace(
        name="Maria's Bistro",
        slug="marias-bistro",
        owner_id=user.id,
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    assert workspace.id is not None
    assert workspace.owner_id == user.id
    assert workspace.subscription_tier == "free"

    # 3. Fill out restaurant profile
    profile = RestaurantProfile(
        workspace_id=workspace.id,
        restaurant_name="Maria's Bistro",
        cuisine_type="Italian",
        description="Cozy Italian bistro with homemade pasta.",
        address="123 Olive Street, Chicago, IL 60601",
        phone="312-555-0199",
        email="contact@mariasbistro.com",
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    assert profile.id is not None
    assert profile.workspace_id == workspace.id
    assert profile.restaurant_name == "Maria's Bistro"

    # 4. Fill out weekly schedule (Mon–Fri open, Sat–Sun closed)
    DAYS = [
        (0, time(11, 0), time(22, 0), False),  # Monday
        (1, time(11, 0), time(22, 0), False),  # Tuesday
        (2, time(11, 0), time(22, 0), False),  # Wednesday
        (3, time(11, 0), time(22, 0), False),  # Thursday
        (4, time(11, 0), time(23, 0), False),  # Friday
        (5, None,        None,        True),   # Saturday – closed
        (6, None,        None,        True),   # Sunday   – closed
    ]

    schedules = []
    for day, open_t, close_t, closed in DAYS:
        entry = WeeklySchedule(
            workspace_id=workspace.id,
            day_of_week=day,
            open_time=open_t,
            close_time=close_t,
            is_closed=closed,
        )
        db.add(entry)
        schedules.append(entry)

    db.commit()
    for s in schedules:
        db.refresh(s)

    assert len(schedules) == 7

    open_days  = [s for s in schedules if not s.is_closed]
    closed_days = [s for s in schedules if s.is_closed]

    assert len(open_days) == 5
    assert len(closed_days) == 2

    # Verify Friday closes at 11pm
    friday = next(s for s in schedules if s.day_of_week == 4)
    assert friday.close_time == time(23, 0)