from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])

# ---------- SCHEMAS ----------
class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str

class LoginSchema(BaseModel):
    email: str
    password: str


# ---------- REGISTER ----------
@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    try:
        user = User(
            username=data.username,
            email=data.email,
            password=hash_password(data.password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )

    # Added "sub" for username
    token = create_token({"user_id": user.id, "sub": user.username})
    return {"token": token, "username": user.username}


# ---------- LOGIN ----------
@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Added "sub" for username
    token = create_token({"user_id": user.id, "sub": user.username})
    return {"token": token, "username": user.username}
