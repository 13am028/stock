import json

from app import app
from model.locations_utils import get_all_locations
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


def test_product_to_stock():
    """Test adding product to stock."""
    uri = "/product-to-stock"
    lid = get_lid()
    pid = get_pid()
    res_success = app.test_client().post(
        uri,
        data=json.dumps({"lid": lid, "pid": pid, "stock": 0}),
        content_type=content_type_json,
    )
    assert res_success.status_code == 200


def test_increase_stock():
    """Test increasing stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post(
        "/increase",
        data=json.dumps({"lid": lid, "pid": pid}),
        content_type=content_type_json,
    )
    assert res.status_code == 200


def test_decrease_stock():
    """Test decreasing stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post(
        "/decrease",
        data=json.dumps({"lid": lid, "pid": pid}),
        content_type=content_type_json,
    )
    assert res.status_code == 200


def test_delete_from_stock():
    """Test deleting product from stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post(
        "/delete-from-stock",
        data=json.dumps({"lid": lid, "pid": pid}),
        content_type=content_type_json,
    )
    assert res.status_code == 200
