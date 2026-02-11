from sqlalchemy.orm import Session
from app.models.productModel import Products
from app.schemas.productSchema import ProductRequest
from decimal import Decimal

def add_product(product: ProductRequest, db: Session):
    new_product = Products(
        product_name=product.product_name,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_all_products(db: Session):
    return db.query(Products).all()


def get_product_by_id(product_id: int, db: Session):
    return db.query(Products).filter(Products.id == product_id).first()


def update_price(product_id: int, price: Decimal, db: Session):
    product = get_product_by_id(product_id, db)
    if not product:
        return None

    product.price = price
    db.commit()
    db.refresh(product)
    return product


def update_stock(product_id: int, stock: int, db: Session):
    product = get_product_by_id(product_id, db)
    if not product:
        return None

    product.stock = stock
    db.commit()
    db.refresh(product)
    return product


def update_price_stock(product_id: int, price: float, stock: int, db: Session):
    product = get_product_by_id(product_id, db)
    if not product:
        return None

    product.price = price
    product.stock = stock
    db.commit()
    db.refresh(product)
    return product


def delete_product(product_id: int, db: Session):
    product = get_product_by_id(product_id, db)
    if not product:
        return None

    db.delete(product)
    db.commit()
    return True
