from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import Base, engine, get_db
from models import User

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS (allow all for testing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic schema for creating users
class UserCreate(BaseModel):
    name: str
    email: str

@app.get("/")
def root():
    return {"message": "FastAPI backend is running 🚀", "docs_url": "/docs"}

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/")
def home():
    return {"message": "FastAPI backend is running 🚀", "docs_url": "/docs"}

