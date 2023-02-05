import json

from app import app
from model.locations_utils import get_all_locations
from model.model import Products, Stock, session
from model.products_utils import get_all_products

product_not_found = "Product Not Found !"
stock_uri = "/stock/"
parser = "html.parser"
content_type_json = "application/json"


def get_lid() -> str:
    """Get the first location_id found."""
    lid = str(get_all_locations()[0].id)
    return lid


def get_pid() -> str:
    """Get the first product_id found."""
    pid = get_all_products()[0].id
    return pid


def get_stock(lid: str, pid: str) -> int:
    return (
        session.query(Stock, Products)
        .join(Products)
        .filter(Stock.location_id == lid and Products.id == pid)
        .first()[0]
        .stock
    )


def test_product_to_stock():
    """Test adding product to stock."""
    uri = "/product-to-stock"
    lid = get_lid()
    pid = get_pid()
    app.test_client().post(
        uri,
        data=json.dumps({"lid": lid, "pid": pid, "stock": 0}),
        content_type=content_type_json,
    )
    products = (
        session.query(Stock, Products)
        .join(Products)
        .filter(Stock.location_id == lid)
        .all()
    )
    assert pid in [product.id for stock, product in products]


def test_increase_stock():
    """Test increasing stock."""
    lid = get_lid()
    pid = get_pid()
    stock = get_stock(lid, pid)
    app.test_client().post(
        "/increase",
        data=json.dumps({"lid": lid, "pid": pid}),
        content_type=content_type_json,
    )
    new_stock = get_stock(lid, pid)
    assert stock + 1 == new_stock


def test_decrease_stock():
    """Test decreasing stock."""
    lid = get_lid()
    pid = get_pid()
    stock = get_stock(lid, pid)
    app.test_client().post(
        "/decrease",
        data=json.dumps({"lid": lid, "pid": pid}),
        content_type=content_type_json,
    )
    new_stock = get_stock(lid, pid)
    assert stock - 1 == new_stock


def test_delete_from_stock():
    """Test deleting product from stock."""
    lid = get_lid()
    pid = get_pid()
    app.test_client().post(
        "/delete-from-stock",
        data=json.dumps({"lid": lid, "pid": pid}),
        content_type=content_type_json,
    )
    assert (
        session.query(Stock, Products)
        .join(Products)
        .filter(Stock.location_id == lid and Products.id == pid)
        .first()
        is None
    )
