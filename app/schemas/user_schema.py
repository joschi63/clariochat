from sqlmodel import SQLModel

class UserSchema(SQLModel):
    name: str
    phone_number: str
    password: str

class UserCreate(UserSchema):
    pass   

class UserRead(UserSchema):
    id: int
    name: str
    