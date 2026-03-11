from app.database import Base
from app.models import (
    chat, restaurant, special_schedule, user, weekly_schedule, workspace
)
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
print("Tables created!")