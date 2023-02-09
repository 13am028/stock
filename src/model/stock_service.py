from typing import Any, List

from model.model import Products, Stock, db
from model.timeline_service import TimelineService

product_not_found = "Product Not Found !"


class StockService:
    """Class containing methods for Stock."""

    @classmethod
    def find_product(cls, location_id: str, product_id: str) -> Stock:
        """Find the product with given location id and product id."""
        return (
            Stock.query.filter(Stock.location_id == location_id)
            .filter(Stock.product_id == product_id)
            .first()
        )

    @classmethod
    def add_product_to_stock(
        cls, location_id: str, product_id: str, stock_num: str
    ) -> str:
        """Add product to stock. If it already exists, change the number of stock."""
        stock = int(stock_num)
        new_stock: Stock = Stock(
            location_id=location_id, product_id=product_id, stock=stock
        )
        if stock < 0:
            return "Stock Cannot Be Negative !"
        products_in_stock: List[Stock] = Stock.query.filter(
            Stock.location_id == location_id
        ).all()
        TimelineService.add_to_timeline(location_id, product_id, stock)
        with db.session() as session:
            for product in products_in_stock:
                if product_id == str(product.product_id):
                    product.stock = stock
                    session.commit()
            session.add(new_stock)
            session.commit()

    @classmethod
    def increase_stock(cls, location_id: str, product_id: str) -> str:
        """Increase stock of a product in location."""
        product: Products = StockService.find_product(location_id, product_id)
        if product is None:
            return product_not_found
        TimelineService.add_to_timeline(location_id, product_id, product.stock + 1)
        product.stock += 1
        with db.session() as session:
            session.commit()

    @classmethod
    def decrease_stock(cls, location_id: str, product_id: str) -> str:
        """Decrease stock of a product in location."""
        product: Products = StockService.find_product(location_id, product_id)
        if product is None:
            return product_not_found
        if product.stock > 0:
            product.stock -= 1
        TimelineService.add_to_timeline(location_id, product_id, product.stock - 1)
        with db.session() as session:
            session.commit()

    @classmethod
    def delete_stock(cls, location_id: str, product_id: str) -> str:
        """Delete product from location stock."""
        product: Products = StockService.find_product(location_id, product_id)
        if product is None:
            return product_not_found
        with db.session() as session:
            session.delete(product)
            session.commit()

    @classmethod
    def get_products(cls, lid: str) -> List[Any]:
        """Get all products given location id."""
        with db.session() as session:
            ret: List[Any] = (
                session.query(Stock, Products)
                .join(Products)
                .filter(Stock.location_id == lid)
                .all()
            )
        ret.sort(key=lambda x: x[1].product_name)
        return ret
