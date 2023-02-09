import json
from typing import Any, List

import path
from app import app
from model.locations_service import LocationService
from model.model import Products, Stock, db
from model.products_service import ProductService
from model.stock_service import StockService

content_type_json = "application/json"


def get_location_id_product_id() -> (int, int):
    """Get the first location_id found."""
    stock = Stock.query.first()
    location_id = stock.location_id
    product_id = stock.product_id
    return location_id, product_id


def get_stock_product(lid: int) -> List[Any]:
    return (
        db.session.query(Stock, Products)
        .join(Products)
        .filter(Stock.location_id == lid)
        .all()
    )


client = app.test_client()


class TestStockRoute:
    """Test /stock routes."""

    def test_product_to_stock(self):
        """Test adding product to stock."""
        location_id = LocationService.get_all_locations()[-1].id
        product_id = ProductService.get_all_products()[-1].id
        client.post(
            path.ADD_PRODUCT_TO_STOCK_PATH,
            data=json.dumps(
                {"location_id": location_id, "product_id": product_id, "stock": 0}
            ),
            content_type=content_type_json,
        )
        products = get_stock_product(location_id)
        assert product_id in [product.id for stock, product in products]
        client.post(
            path.ADD_PRODUCT_TO_STOCK_PATH,
            data=json.dumps(
                {"location_id": location_id, "product_id": product_id, "stock": 10}
            ),
            content_type=content_type_json,
        )
        products = get_stock_product(location_id)
        for stock, product in products:
            if product.id == product_id:
                assert stock.stock == 10

    def test_increase_stock(self):
        """Test increasing stock."""
        location_id, product_id = get_location_id_product_id()
        stock = StockService.find_stock(location_id, product_id).stock
        client.put(
            path.INCREASE_STOCK_PATH,
            data=json.dumps({"location_id": location_id, "product_id": product_id}),
            content_type=content_type_json,
        )
        new_stock = StockService.find_stock(location_id, product_id).stock
        assert stock + 1 == new_stock

    def test_decrease_stock(self):
        """Test decreasing stock."""
        location_id, product_id = get_location_id_product_id()
        stock = StockService.find_stock(location_id, product_id).stock
        client.put(
            path.DECREASE_STOCK_PATH,
            data=json.dumps({"location_id": location_id, "product_id": product_id}),
            content_type=content_type_json,
        )
        new_stock = StockService.find_stock(location_id, product_id).stock
        assert stock - 1 == new_stock

    def test_delete_from_stock(self):
        """Test deleting product from stock."""
        location_id, product_id = get_location_id_product_id()
        client.delete(
            path.DELETE_PRODUCT_FROM_STOCK_PATH,
            data=json.dumps({"location_id": location_id, "product_id": product_id}),
            content_type=content_type_json,
        )
        assert StockService.find_stock(location_id, product_id) is None
