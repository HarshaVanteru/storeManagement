from typing import Annotated
from fastapi import Depends
from jose import jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

SECRET_KEY = "dnidhisgnslgnalshjhsggeeehbds"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30
def create_access_token(data:dict):
    to_encode = data.copy()
    expiry_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode["exp"] = expiry_time
    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

