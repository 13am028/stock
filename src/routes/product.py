"""Route and methods for products."""
from flask import Blueprint, Response, make_response, request

from model import products_utils

product = Blueprint("product", __name__)


@product.route("/add-product", methods=["POST"])
def add_product() -> Response:
    """Add a new product."""
    product_name = request.json["product"]
    ret: str = products_utils.add_product(product_name)
    return make_response(ret, 200)


@product.route("/delete-product", methods=["POST"])
def delete_product() -> Response:
    """Delete product."""
    pid: str = request.json["pid"]
    ret: str = products_utils.delete_product(pid)
    return make_response(ret, 200)
