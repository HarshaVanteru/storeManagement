from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException
from app.models.users import User
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

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/app/api/v1/users/signin"
)

token = Annotated[str,Depends(oauth2_scheme)]


def create_access_token(data:dict):
    to_encode = data.copy()
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode["exp"] = expiry_time
    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return token

def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def get_current_user(token:token,db:db_dependency):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401,detail="details not found")
    user = db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401,detail="details not found")
    return user


def admin_required(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user

