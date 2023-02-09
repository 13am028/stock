"""Route and methods for products."""
from flask import Blueprint, Response, make_response, request

from model.products_service import ProductService
from path import ADD_PRODUCT_PATH, DELETE_PRODUCT_PATH

product = Blueprint("product", __name__)


@product.route(ADD_PRODUCT_PATH, methods=["POST"])
def add_product() -> Response:
    """Add a new product."""
    product_name = request.json["product"]
    ret: str = ProductService.add_product(product_name)
    return make_response({"message": ret}, 200)


@product.route(DELETE_PRODUCT_PATH, methods=["POST"])
def delete_product() -> Response:
    """Delete product."""
    pid: str = request.json["pid"]
    ret: str = ProductService.delete_product(pid)
    return make_response({"message": ret}, 200)
