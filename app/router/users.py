from fastapi import APIRouter, Depends, HTTPException
from ..database.models import User, ChatUser
from ..database.database import SessionDep
from ..schemas.user_schema import UserCreate, UserRead
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from argon2 import PasswordHasher

router = APIRouter(prefix="/users", tags=["users"])
ph = PasswordHasher()

@router.post("/create", response_model=UserRead)
def create_user(user: UserCreate, session: SessionDep):
    db_user = session.exec(select(User).where(User.phone_number == user.phone_number)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    user.password = ph.hash(user.password)
    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@router.get("/get/{user_id}")
def read_user(user_id: int, session: SessionDep):
    db_user = session.exec(select(User).where(User.id == user_id).options(selectinload(User.chats))).first() # type: ignore
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user