import secrets
import string
from typing import List

from app import app
from model import Stock
from services.products_service import ProductService
from services.stock_service import StockService


def get_random_string(length: int) -> str:
    """Get a random string."""
    result_str = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return result_str


class TestStockService:
    """Class containing methods for Stock."""

    with app.app_context():

        def test_find_product(self):
            """Find the product with given location id and product id."""
            StockService.add_product_to_stock(1, 1, 1)
            assert isinstance(StockService.find_stock(1, 1), Stock)

        def test_add_product_to_stock(self):
            """Test adding product to location aka.stock."""
            assert StockService.add_product_to_stock(1, 1, 20).stock == 20
            new_product = ProductService.add_product(get_random_string(5))
            assert StockService.add_product_to_stock(1, new_product.id, 99).stock == 99

        def test_increase_stock(self):
            """Increase stock of a product in location."""
            old_stock = StockService.find_stock(1, 1).stock
            assert StockService.increase_stock(1, 1).stock == old_stock + 1

        def test_decrease_stock(self):
            """Decrease stock of a product in location."""
            old_stock = StockService.find_stock(1, 1).stock
            assert StockService.decrease_stock(1, 1).stock == old_stock - 1

        def test_delete_stock(self):
            """Delete product from location stock."""
            stock = StockService.add_product_to_stock(1, 1, 1)
            assert StockService.delete_stock(1, 1).id == stock.id

        def test_get_products(self):
            """Test getting all products given vending machine location id."""
            assert isinstance(StockService.get_products(1), List)
