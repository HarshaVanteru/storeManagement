
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String(50),unique=True,nullable=False)
    first_name = Column(String(50),nullable=False)
    last_name = Column(String(50),nullable=True)
    email = Column(String(100),unique=True,index=True,nullable=False)
    hashed_password = Column(String(400),nullable=False)
    role = Column(String(50),nullable=False,default="user")
    is_active = Column(Boolean,nullable=False,default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now()
    )

