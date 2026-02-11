from typing import Annotated, List
from decimal import Decimal
from fastapi import APIRouter, status, Path, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.repositories.productRepo import (
    add_product,
    get_all_products,
    get_product_by_id,
    update_stock,
    delete_product,
    update_price, update_price_stock
)
from app.schemas.productSchema import ProductRequest, ProductResponse

router = APIRouter(prefix="/product")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/",status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def add_product_route(product: ProductRequest,
                            db: db_dependency):
    return add_product(product, db)

@router.get("/",response_model=List[ProductResponse])
async def get_all_products_route(db: db_dependency):
    products = get_all_products(db)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products


@router.get("/{id}",response_model=ProductResponse)
async def get_product_by_id_route(db: db_dependency,
                                  id: int = Path(gt=0)):
    product = get_product_by_id(id, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/stock/{id}/{stock}",status_code=status.HTTP_204_NO_CONTENT)
async def update_stock_route(db: db_dependency ,
                             id: int = Path(gt=0),
                             stock: int = Path(ge=1)
                             ):
    product = update_stock(id, stock, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

@router.put("/price/{id}/{price}",status_code=status.HTTP_204_NO_CONTENT)
async def update_price_route(db: db_dependency ,
                             id: int = Path(gt=0),
                             price:Decimal = Path(ge=1)
                             ):
    product = update_price(id, price, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

@router.put("/{id}/{stock}/{price}",status_code=status.HTTP_204_NO_CONTENT)
async def update_stock_price_route(db: db_dependency ,
                             id: int = Path(gt=0),
                             stock: int = Path(ge=1),
                             price: Decimal = Path(ge=0)
                             ):
    product = update_price_stock(id,price, stock, db)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_route(db:db_dependency,id:int = Path(gt=0)):
    product = delete_product(id,db)
    if not product:
        raise HTTPException(status_code=404,detail="Product not found")