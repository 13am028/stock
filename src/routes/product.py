"""Route and methods for products."""
from flask import Blueprint, Response, make_response, request

import html_methods
from model.products_service import ProductService
from path import ADD_PRODUCT_PATH, DELETE_PRODUCT_PATH

product = Blueprint("product", __name__)


@product.route(ADD_PRODUCT_PATH, methods=[html_methods.POST])
def add_product() -> Response:
    """Add a new product."""
    product_name: str = request.json["product_name"]
    ret: str = ProductService.add_product(product_name)
    return make_response({"message": ret}, 200)


@product.route(DELETE_PRODUCT_PATH, methods=[html_methods.DELETE])
def delete_product() -> Response:
    """Delete product."""
    product_id: str = request.json["product_id"]
    ret: str = ProductService.delete_product(product_id)
    return make_response({"message": ret}, 200)
