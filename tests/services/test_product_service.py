import secrets
import string
from typing import List

from app import app
from model import Products
from services.products_service import ProductService


def get_random_string(length: int) -> str:
    """Get a random string."""
    result_str = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return result_str


class TestProductService:
    """Class containing methods for Product."""

    with app.app_context():

        def test_get_all_products(self):
            """Get all products."""
            assert isinstance(ProductService.get_all_products(), List)

        def test_add_product(self):
            """Add new product."""
            product_name = get_random_string(5)
            assert isinstance(ProductService.add_product(product_name), Products)

        def test_delete_product(self):
            """Delete product."""
            product_name = get_random_string(5)
            product = ProductService.add_product(product_name)
            assert ProductService.delete_product(product.id) == product
