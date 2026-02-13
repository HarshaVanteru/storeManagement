from typing import Annotated, List
from fastapi import APIRouter, status, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.dependency import db_dependency
from app.repositories.productRepo import (
    add_product,
    get_all_products,
    get_product_by_id,
    delete_product,
    update_product
)
from app.schemas.productSchema import (
    ProductRequest,
    ProductResponse,
    ProductUpdate
)

router = APIRouter(prefix="/product", tags=["Product"])





@router.post("/",status_code=status.HTTP_201_CREATED,response_model=ProductResponse)
async def add_product_route(product: ProductRequest, db: db_dependency):
    return add_product(product, db)



@router.get("/",response_model=List[ProductResponse])
async def get_all_products_route(db: db_dependency):
    return get_all_products(db)



@router.get("/{id}",response_model=ProductResponse)
async def get_product_by_id_route(id: int = Path(gt=0),db: db_dependency = None):
    product = get_product_by_id(id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.patch("/{id}",response_model=ProductResponse)
async def update_product_route(id: int = Path(gt=0),product: ProductUpdate = None,db: db_dependency = None):
    updated_product = update_product(id, product, db)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_route(id: int = Path(gt=0),db: db_dependency = None):
    product = delete_product(id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
