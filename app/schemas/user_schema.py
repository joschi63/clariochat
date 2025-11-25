from sqlmodel import SQLModel

class UserSchema(SQLModel):
    name: str
    email: str
    phone_number: str

class UserCreate(UserSchema):
    pass   

class UserRead(UserSchema):
    id: int
    name: str
    