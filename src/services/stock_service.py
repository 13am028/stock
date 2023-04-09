from typing import Any, List

from model import Products, Stock, session
from services.timeline_service import TimelineService


class StockService:
    """Class containing methods for Stock."""

    @classmethod
    def find_stock(cls, location_id: int, product_id: int) -> Stock:
        """Find the product with given location id and product id."""
        return (
            Stock.query.filter(Stock.location_id == location_id)
            .filter(Stock.product_id == product_id)
            .first()
        )

    @classmethod
    def add_product_to_stock(
        cls, location_id: int, product_id: int, stock: int
    ) -> Stock:
        """Add product to stock. If it already exists, change the number of stock."""
        TimelineService.add_to_timeline(location_id, product_id, stock)
        product_in_stock: Stock = (
            Stock.query.filter(Stock.location_id == location_id)
            .filter(Stock.product_id == product_id)
            .first()
        )
        if product_in_stock is not None:
            product_in_stock.stock = stock
            session.commit()
            return product_in_stock
        else:
            new_stock: Stock = Stock(
                location_id=location_id, product_id=product_id, stock=stock
            )
            session.add(new_stock)
            session.commit()
            return new_stock

    @classmethod
    def increase_stock(cls, location_id: int, product_id: int) -> Stock:
        """Increase stock of a product in location."""
        stock: Stock = StockService.find_stock(location_id, product_id)
        TimelineService.add_to_timeline(location_id, product_id, stock.stock + 1)
        stock.stock += 1
        session.commit()
        return stock

    @classmethod
    def decrease_stock(cls, location_id: int, product_id: int) -> Stock:
        """Decrease stock of a product in location."""
        stock: Stock = StockService.find_stock(location_id, product_id)
        stock.stock -= 1
        TimelineService.add_to_timeline(location_id, product_id, stock.stock - 1)
        session.commit()
        return stock

    @classmethod
    def delete_stock(cls, location_id: int, product_id: int) -> Stock:
        """Delete product from location stock."""
        stock: Stock = StockService.find_stock(location_id, product_id)
        session.delete(stock)
        session.commit()
        return stock

    @classmethod
    def get_products(cls, location_id: int) -> List[Any]:
        """Get all products given location id."""
        ret: List[Any] = (
            session.query(Stock, Products)
            .join(Products)
            .filter(Stock.location_id == location_id)
            .all()
        )
        ret.sort(key=lambda x: x[1].product_name)
        return ret
