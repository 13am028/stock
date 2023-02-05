from typing import List

from model.model import Products, session


def get_all_products() -> List[Products]:
    """Get all products."""
    return Products.query.all()


def add_product(product_name: str):
    """Add new product."""
    new_product: Products = Products(product_name=product_name)
    session.add(new_product)
    session.commit()


def delete_product(pid: str):
    """Delete product."""
    del_product = Products.query.filter(Products.id == pid).first()
    session.delete(del_product)
    session.commit()
