from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..database.models import User
from ..database.database import SessionDep
from ..schemas.user_schema import UserCreate, UserRead
from sqlmodel import Session, select
from argon2 import PasswordHasher
from ..security.token_managing import get_current_user

router = APIRouter()
ph = PasswordHasher()

@router.get("/login")
def login(user: User = Depends(get_current_user), form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        ph.verify(user.password, form_data.password)
    except:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )
    return {"message": f"Welcome {user.name}!"}