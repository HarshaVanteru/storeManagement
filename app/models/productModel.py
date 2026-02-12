from app.core.database import Base
from sqlalchemy import Integer,Column,String,DECIMAL


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,index=True)

    product_name = Column(String(255), nullable=False, unique=True)

    price = Column(DECIMAL(10, 2), nullable=False)

    stock = Column(Integer, default=1, nullable=False)

