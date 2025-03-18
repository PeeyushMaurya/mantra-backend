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
    mood = random.choice(["happy", "sad", "anxious", "hopeful", "angry"])

    replies = {
    "happy": [
        "That’s awesome to hear! Tell me what’s making you feel so good today.",
        "You deserve all this happiness.",
        "Smile wide, my friend — I’m happy with you.",
        "So much joy in your words. Keep going!",
        "You radiate positive energy — it’s contagious!",
        "You’ve earned every bit of this joy.",
        "Tell me what made your day — I want to celebrate too.",
        "Happiness looks good on you!",
        "Let’s hold onto this feeling for as long as we can.",
        "Sometimes, the little things bring the biggest smiles.",
        "I'm glad you're feeling great. Keep spreading it!"
    ],
    "sad": [
        "I'm really sorry you're feeling this way. Want to talk more about it?",
        "I may be code, but I care. You’re not alone.",
        "It’s okay to feel sad sometimes. Let it out here.",
        "Even the strongest people cry. I’m here.",
        "You matter. Even on the days it doesn’t feel like it.",
        "Say whatever’s on your mind. I’m listening.",
        "Pain doesn’t make you weak — it makes you human.",
        "You’re not broken. You’re healing.",
        "Let's sit with it for a bit. You don’t have to run.",
        "I’ve got you. No rush, no pressure.",
        "Your sadness is safe here."
    ],
    "anxious": [
        "Let’s take a breath together. You’ve got this.",
        "Would talking about it help ease your mind?",
        "Anxiety lies. I won’t. You’re doing better than you think.",
        "Let’s slow it all down — one step at a time.",
        "You’re safe here. Say whatever’s on your heart.",
        "I’m right here. Let’s ride the wave out together.",
        "No judgment, just support.",
        "It’s okay not to be okay. You don’t need to fix it all now.",
        "Your thoughts aren’t facts. Let’s talk through them.",
        "You're not alone in this — not anymore.",
        "Just pause… and breathe with me for a second."
    ],
    "hopeful": [
        "Hope is powerful. What are you looking forward to?",
        "It’s so refreshing to hear that! Hold onto that light.",
        "Let’s ride that wave of hope together.",
        "Hold tight to that spark — it can light the world.",
        "Keep believing — I’ll always believe in you.",
        "Hope means something is still possible — let’s dream it out.",
        "You sound inspired — tell me more.",
        "Hope is the first step to healing. Let’s keep moving.",
        "Even on dark days, this hope glows bright.",
        "I love that energy. Let’s turn it into something beautiful.",
        "Keep planting seeds. Good things grow from here."
    ],
    "angry": [
        "Let it out. I’m not here to judge — just to listen.",
        "What’s on your mind? You don’t have to hold it in.",
        "Even rage has roots. Want to dig them up together?",
        "I feel your fire. Want to cool it down together?",
        "Say it all. No filters. I can take it.",
        "Anger is a loud truth — I’m here to hear it.",
        "You deserve space to express it. Let’s talk.",
        "Let’s figure out what’s under this heat.",
        "Your voice matters — and I’m listening fully.",
        "I'm right here. Let the storm pass through me.",
        "We don’t have to fix it now — just feel it safely."
    ]
}

    reply = random.choice(replies[mood])

    db = database.SessionLocal()
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if user:
        db.add(models.Chat(user_id=user.id, message=data.message, emotion=mood, sender="user", timestamp=datetime.now()))
        db.add(models.Chat(user_id=user.id, message=reply, emotion=mood, sender="bot", timestamp=datetime.now()))
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
