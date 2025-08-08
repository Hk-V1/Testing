from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import User

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
