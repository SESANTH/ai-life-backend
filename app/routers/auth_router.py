from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.auth import hash_password, verify_password, create_token

router = APIRouter()

@router.post("/signup")
def signup(email: str, password: str, db: Session = Depends(get_db)):
    user = User(email=email, password=hash_password(password))
    db.add(user)
    db.commit()
    return {"message": "User created"}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        return {"error": "Invalid credentials"}

    token = create_token({"user_id": user.id})

    return {"token": token}