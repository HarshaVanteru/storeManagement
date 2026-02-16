

from pydantic import BaseModel, Field
from decimal import Decimal
from pydantic import field_validator

class ProductRequest(BaseModel):
    product_name: str = Field(..., min_length=3, max_length=255)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    stock: int = Field(..., ge=0)

    @field_validator("product_name")
    def remove_spaces(cls, v):
        if not v.strip():
            raise ValueError("Product name cannot be empty")
        return v.strip()


class ProductResponse(BaseModel):
    id: int
    product_name: str
    price: Decimal
    stock: int

    class Config:
        from_attributes = True



class ProductUpdate(BaseModel):
    stock: int | None = Field(default=None, gt=0,max_digits=5)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)

