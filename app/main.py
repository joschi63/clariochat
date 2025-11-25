from fastapi import FastAPI
from .database.database import create_db_and_tables
from .router import user

create_db_and_tables()

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}
