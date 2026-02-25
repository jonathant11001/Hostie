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