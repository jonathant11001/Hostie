from fastapi import FastAPI
from .database import engine, Base
from .routes import restaurants, chat, users
from app import models  #

app = FastAPI(title="Hostie Backend")

print("Attempting to create tables with SQLAlchemy...")
Base.metadata.create_all(bind=engine)
print("Tables creation attempted.")

app.include_router(restaurants.router)
app.include_router(chat.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}