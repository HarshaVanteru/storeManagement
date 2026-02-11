from app.core.database import Base
from sqlalchemy import Integer,Column,String,DECIMAL


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,index=True)
    product_name = Column(String(255),nullable=False)
    price = Column(DECIMAL,nullable=False)
    stock = Column(Integer,default=1)
