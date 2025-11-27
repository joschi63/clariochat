from sqlmodel import SQLModel
from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    phone_number: str
    password: str

class UserCreate(UserSchema):
    pass   

class UserRead(UserSchema):
    id: int
    name: str
    