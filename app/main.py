from fastapi import FastAPI
from .database.database import create_db_and_tables
from .router import user
from .router import auth

create_db_and_tables()

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
