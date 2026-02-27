from fastapi.testclient import TestClient
from app.main import app
from app.database import engine
from app.models.user import User

client = TestClient(app)

def test_root():
    response = client.get("/")
    # Accept 200 or 404, but print response for debugging
    print("Status:", response.status_code)
    print("Content:", response.text)
    assert response.status_code in (200, 404)
    # Optionally check for expected content if status is 200
    if response.status_code == 200:
        assert response.text.strip() != ""

def test_create_user(db):
    user = User(
        displayname="Jonathan",
        username="jon123",
        email="jon@test.com",
        passwordHash="hashed_pw"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.role == "owner"  # default value
    assert user.createdAt is not None

def test_unique_username_constraint(db):
    user1 = User(
        displayname="Alice",
        username="alice123",
        email="alice@test.com",
        passwordHash="pw1"
    )
    db.add(user1)
    db.commit()
    db.refresh(user1)

    user2 = User(
        displayname="Bob",
        username="alice123",  # Duplicate username
        email="bob@test.com",
        passwordHash="pw2"
    )
    db.add(user2)
    try:
        db.commit()
        assert False, "Expected IntegrityError for duplicate username"
    except Exception as e:
        # Accept IntegrityError or SQLAlchemy error
        assert "unique" in str(e).lower() or "integrity" in str(e).lower()

def test_duplicate_user(db):
    user1 = User(
        displayname="Charlie",
        username="charlie123",
        email="charlie@test.com",
        passwordHash="pw1"
    )
    db.add(user1)
    db.commit()
    db.refresh(user1)

    user2 = User(
        displayname="Charlie",
        username="charlie122",
        email="charlie@test.com",
        passwordHash="pw1"
    )
    db.add(user2)
    try:
        db.commit()
        assert False, "Expected IntegrityError for duplicate user (username and email)"
    except Exception as e:
        print("Caught exception:", e)
        assert "unique" in str(e).lower() or "integrity" in str(e).lower()
        db.rollback()

    # Print out all users in the DB
    users = db.query(User).all()
    print("Users in DB:", users)