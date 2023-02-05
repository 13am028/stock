import json
import secrets
import string

from app import app
from model.products_utils import get_all_products

product_uri = "/products"
parser = "html.parser"


def get_random_string(length: int) -> str:
    """Get a random string."""
    result_str = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return result_str


def get_pid() -> str:
    """Get the first product_id found."""
    pid = get_all_products()[0].id
    return pid


def test_add_product() -> None:
    """Test adding a new product."""
    product_name = get_random_string(7)
    app.test_client().post(
        "/add-product",
        data=json.dumps({"product": product_name}),
        content_type="application/json",
    )
    assert product_name in [product.product_name for product in get_all_products()]


def test_delete_product() -> None:
    """Test deleting product."""
    pid = get_pid()
    app.test_client().post(
        "/delete-product",
        data=json.dumps({"pid": pid}),
        content_type="application/json",
    )
    assert pid not in [product.id for product in get_all_products()]