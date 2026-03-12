from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import restaurants, chat, users
from app import models  #

app = FastAPI(title="Hostie Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(restaurants.router)
app.include_router(chat.router)
app.include_router(users.router)


@app.get("/health")
def health():
    return {"status": "ok"}