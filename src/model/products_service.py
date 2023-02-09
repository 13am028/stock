from typing import List

from model.model import Products, session


class ProductService:
    """Class containing methods for Product."""

    @classmethod
    def get_all_products(cls) -> List[Products]:
        """Get all products."""
        return Products.query.all()

    @classmethod
    def add_product(cls, product_name: str) -> Products:
        """Add new product."""
        new_product: Products = Products(product_name=product_name)
        session.add(new_product)
        session.commit()
        return new_product

    @classmethod
    def delete_product(cls, product_id: int) -> Products:
        """Delete product."""
        del_product = Products.query.filter(Products.id == product_id).first()
        session.delete(del_product)
        session.commit()
        return del_product
