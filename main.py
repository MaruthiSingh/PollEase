from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = "sqlite:///./polls.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

INSTALLED_APPS = [
    'corsheaders',
    ...
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Frontend React app
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow all origins (Change this for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey("polls.id"))
    text = Column(String)
    votes = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class PollCreate(BaseModel):
    question: str
    options: list[str]

class Vote(BaseModel):
    option_id: int

@app.post("/polls/")
def create_poll(poll: PollCreate, db: Session = Depends(get_db)):
    new_poll = Poll(question=poll.question)
    db.add(new_poll)
    db.commit()
    db.refresh(new_poll)
    
    for option_text in poll.options:
        new_option = Option(poll_id=new_poll.id, text=option_text)
        db.add(new_option)
    db.commit()
    
    return {"poll_id": new_poll.id}

@app.post("/vote/")
def vote(vote: Vote, db: Session = Depends(get_db)):
    option = db.query(Option).filter(Option.id == vote.option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option not found")
    option.votes += 1
    db.commit()
    return {"message": "Vote cast successfully"}

@app.get("/polls/{poll_id}/results/")
def get_results(poll_id: int, db: Session = Depends(get_db)):
    poll = db.query(Poll).filter(Poll.id == poll_id).first()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found")
    options = db.query(Option).filter(Option.poll_id == poll_id).all()
    return {"question": poll.question, "options": [{"id": opt.id, "text": opt.text, "votes": opt.votes} for opt in options]}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific frontend URL for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
