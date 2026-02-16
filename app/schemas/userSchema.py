from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserSignupForm(BaseModel):
    username:str = Field(min_length=3,max_length=50)
    first_name:str = Field(min_length=1,max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email:EmailStr
    password:str = Field(min_length=5,max_length=128)



class UserData(BaseModel):
    username: str
    first_name: str
    last_name: Optional[str]
    email: EmailStr

    class Config:
        from_attributes = True