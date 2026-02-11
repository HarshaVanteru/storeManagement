from pydantic import BaseModel, Field
from decimal import Decimal


class ProductRequest(BaseModel):
    product_name: str = Field(min_length=3)
    price: Decimal = Field(gt=0)
    stock: int = Field(ge=1)

class ProductResponse(BaseModel):
    id: int
    product_name: str
    price: Decimal
    stock: int

    class Config:
        from_attributes = True
