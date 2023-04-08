import json
import secrets
import string

import path
from app import app
from model import Stock, StockTimeline
from services.products_service import ProductService


def get_random_string(length: int) -> str:
    """Get a random string."""
    result_str = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return result_str


class TestProductRoute:
    """Tests for /product routes."""

    def test_add_product(self) -> None:
        """Test adding a new product."""
        product_name = get_random_string(7)
        app.test_client().post(
            path.ADD_PRODUCT_PATH,
            data=json.dumps({"product_name": product_name}),
            content_type="application/json",
        )
        assert product_name in [
            product.product_name for product in ProductService.get_all_products()
        ]

    def test_delete_product(self) -> None:
        """Test deleting product."""
        product_id = ProductService.add_product(get_random_string(7)).id
        app.test_client().delete(
            path.DELETE_PRODUCT_PATH,
            data=json.dumps({"product_id": product_id}),
            content_type="application/json",
        )
        if product_id in [
            stock.product_id for stock in Stock.query.all()
        ] or product_id in [
            timeline.product_id for timeline in StockTimeline.query.all()
        ]:
            assert product_id in [
                product.id for product in ProductService.get_all_products()
            ]
        else:
            assert product_id not in [
                product.id for product in ProductService.get_all_products()
            ]
