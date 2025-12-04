from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..database.models import User
from ..database.database import SessionDep
from ..schemas.user_schema import UserCreate, UserRead
from sqlmodel import Session, select
from argon2 import PasswordHasher
from ..security.token_managing import create_acces_token, Token
from datetime import timedelta

router = APIRouter()
ph = PasswordHasher()

@router.get("/login")
def login(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = session.exec(select(User).where(User.phone_number == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    try:
        ph.verify(user.password, form_data.password)
    except:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_acces_token(
        data={"sub": user.phone_number}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")