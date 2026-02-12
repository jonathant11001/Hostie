from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import APIKey


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_restaurant(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    api_key = db.query(APIKey).filter(APIKey.key == x_api_key).first()

    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return api_key.restaurant_id