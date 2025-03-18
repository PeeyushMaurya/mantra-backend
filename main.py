from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import random
import database, models

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str

class ChatRequest(BaseModel):
    email: str
    message: str

@app.post("/login")
def login_user(data: LoginRequest):
    db = database.SessionLocal()
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user:
        new_user = models.User(email=data.email)
        db.add(new_user)
        db.commit()
    db.close()
    return {"message": "User logged in"}

@app.post("/chat")
def chat(data: ChatRequest):
    mood = random.choice(["happy", "anxious", "sad", "hopeful"])
    reply = f"I'm here for you. Let's talk more about that."
    db = database.SessionLocal()
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if user:
        chat = models.Chat(user_id=user.id, message=data.message, emotion=mood, sender="user", timestamp=datetime.now())
        response = models.Chat(user_id=user.id, message=reply, emotion=mood, sender="bot", timestamp=datetime.now())
        db.add(chat)
        db.add(response)
        db.commit()
    db.close()
    return {"reply": reply, "emotion": mood}

@app.get("/chat_history")
def chat_history(email: str):
    db = database.SessionLocal()
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return []
    history = db.query(models.Chat).filter(models.Chat.user_id == user.id).all()
    db.close()
    return [{"sender": h.sender, "message": h.message, "emotion": h.emotion} for h in history]

@app.get("/emotion_history")
def emotion_history():
    return {"labels": ["Mon", "Tue", "Wed", "Thu", "Fri"], "values": [3, 2, 4, 5, 1]}
