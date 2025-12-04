from fastapi import APIRouter, Depends, HTTPException
from ..database.models import User
from ..database.database import SessionDep
from ..schemas.user_schema import UserCreate, UserRead
from sqlmodel import Session, select
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