"""Route and methods for products."""
from typing import Dict

from flask import Blueprint, Response, make_response, request

import html_methods
from services.products_service import ProductService
from path import ADD_PRODUCT_PATH, DELETE_PRODUCT_PATH

product = Blueprint("product", __name__)


@product.route(ADD_PRODUCT_PATH, methods=[html_methods.POST])
def add_product() -> Response:
    """Add a new product."""
    product_name: str = request.json["product_name"]
    ret: Dict = ProductService.add_product(product_name).to_dict()
    return make_response(ret, 200)


@product.route(DELETE_PRODUCT_PATH, methods=[html_methods.DELETE])
def delete_product() -> Response:
    """Delete product."""
    product_id: int = request.json["product_id"]
    ret: Dict = ProductService.delete_product(product_id).to_dict()
    return make_response(ret, 200)
