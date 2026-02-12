from sqlalchemy.orm import Session
from app.models.productModel import Products
from app.schemas.productSchema import ProductRequest, ProductUpdate


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


# ✅ Single Clean Update Function
def update_product(product_id: int, product_data: ProductUpdate, db: Session):
    product = get_product_by_id(product_id, db)
    if not product:
        return None

    if product_data.price is not None:
        product.price = product_data.price

    if product_data.stock is not None:
        product.stock = product_data.stock

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
