from fastapi import APIRouter, Depends, HTTPException
from ..database.models import User
from ..database.database import SessionDep
from ..schemas.user_schema import UserCreate, UserRead
from sqlmodel import Session, select

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserRead)
def create_user(user: UserCreate, session: SessionDep):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User.model_validate(user)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user