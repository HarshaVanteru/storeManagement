from typing import List
from fastapi import APIRouter, status, Path, Depends, HTTPException
from app.core.dependency import db_dependency, admin_required
from app.core.dependency import get_current_user
from app.models.users import User

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




@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def add_product_route(
    product: ProductRequest,
    db: db_dependency,
    user: User = Depends(admin_required)
):
    return add_product(product, db)




@router.get("/", response_model=List[ProductResponse])
async def get_all_products_route(
    db: db_dependency,
    current_user: User = Depends(get_current_user)
):
    return get_all_products(db)



@router.get("/{id}", response_model=ProductResponse)
async def get_product_by_id_route(
        db: db_dependency,
        id: int = Path(gt=0),
        current_user: User = Depends(get_current_user)
):
    product = get_product_by_id(id, db)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product




@router.put("/{id}", response_model=ProductResponse)
async def update_product_route(
        product: ProductUpdate,
        db: db_dependency,
        id: int = Path(gt=0),
        user: User = Depends(admin_required)
):
    updated_product = update_product(id, product, db)

    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated_product


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_route(
        db: db_dependency,
        user: User = Depends(admin_required),
        id: int = Path(gt=0)

):
    product = delete_product(id, db)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
