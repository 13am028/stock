from typing import List

from model.model import Products, db


class ProductService:
    """Class containing methods for Product."""

    @classmethod
    def get_all_products(cls) -> List[Products]:
        """Get all products."""
        return Products.query.all()

    @classmethod
    def add_product(cls, product_name: str):
        """Add new product."""
        new_product: Products = Products(product_name=product_name)
        with db.session() as session:
            session.add(new_product)
            session.commit()

    @classmethod
    def delete_product(cls, product_id: str):
        """Delete product."""
        del_product = Products.query.filter(Products.id == product_id).first()
        with db.session() as session:
            session.delete(del_product)
            session.commit()
