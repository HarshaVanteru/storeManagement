from typing import reveal_type

from fastapi import APIRouter,status,HTTPException
from sqlalchemy.sql.functions import current_user

from app.core.security import hash_password, verify_password
from app.schemas.userSchema import   UserSignupForm,UserSigninForm
from app.core.dependency import db_dependency,create_access_token
from app.models.users import User

router = APIRouter(prefix="/users",tags=["user"])



@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def sign_up(db:db_dependency,user_data:UserSignupForm):
    check_user = db.query(User).filter(User.username == user_data.username).first()
    if check_user:
        raise HTTPException(status_code=409,detail="user already found with that username")
    check_user = db.query(User).filter(User.email==user_data.email).first()
    if check_user:
        raise HTTPException(status_code=409, detail="user already found with that email")
    Hash_password = hash_password(user_data.password)
    user = User(username=user_data.username,
                email = user_data.email,
                hashed_password = Hash_password,
                first_name = user_data.first_name,
                last_name= user_data.last_name
                )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message":"user signed up successfully"}


@router.post("/signin", status_code=status.HTTP_200_OK)
async def sign_in(user_data: UserSigninForm, db: db_dependency):

    user = db.query(User).filter(User.email == user_data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )

    token_data = {"id": user.id, "role": user.role}

    return {
        "access_token": create_access_token(token_data),
        "token_type": "bearer"
    }
