"""Route and methods for stock."""
from flask import Blueprint, Response, make_response, request

import html_methods
import path
from model.stock_service import StockService

stock = Blueprint("stock", __name__)
stock_page = "page.stock"

product_not_found = {"message": "Product Not Found !"}


@stock.route(path.ADD_PRODUCT_TO_STOCK_PATH, methods=[html_methods.POST])
def product_to_stock() -> Response:
    """Add a product to stock of current location then redirect back."""
    location_id: int = request.json["location_id"]
    product_id: int = request.json["product_id"]
    stock_num: int = request.json["stock"]
    ret: str = StockService.add_product_to_stock(location_id, product_id, stock_num)
    return make_response({"message": ret}, 200)


@stock.route(path.INCREASE_STOCK_PATH, methods=[html_methods.PUT])
def increase_stock() -> Response:
    """Increase stock of a product then redirect."""
    location_id: int = request.json["location_id"]
    product_id: int = request.json["product_id"]
    ret: str = StockService.increase_stock(location_id, product_id)
    return make_response({"message": ret}, 200)


@stock.route(path.DECREASE_STOCK_PATH, methods=[html_methods.PUT])
def decrease_stock() -> Response:
    """Decrease stock of product then redirect."""
    location_id: int = request.json["location_id"]
    product_id: int = request.json["product_id"]
    ret: str = StockService.decrease_stock(location_id, product_id)
    return make_response({"message": ret}, 200)


@stock.route(path.DELETE_PRODUCT_FROM_STOCK_PATH, methods=[html_methods.DELETE])
def delete_from_stock() -> Response:
    """Delete product from current location stock then redirect."""
    location_id: int = request.json["location_id"]
    product_id: int = request.json["product_id"]
    ret: str = StockService.delete_stock(location_id, product_id)
    return make_response({"message": ret}, 200)
