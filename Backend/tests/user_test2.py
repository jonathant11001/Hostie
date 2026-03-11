from fastapi.testclient import TestClient
from app.main import app
from app.database import engine
from app.models.user import User

client = TestClient(app)

def test_create_another_user(db):
    user = User(
        displayname="Paul",
        username="paul123",
        email="paul@test.com",
        passwordHash="hashed_pw"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    assert user.id is not None
    assert user.role == "owner"
    assert user.createdAt is not None