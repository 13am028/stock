"""Route and methods for stock."""
from flask import Blueprint, Response, make_response, request

import path
from model.stock_service import StockService

stock = Blueprint("stock", __name__)
stock_page = "page.stock"

product_not_found = {"message": "Product Not Found !"}


@stock.route(path.ADD_PRODUCT_TO_STOCK_PATH, methods=["POST"])
def product_to_stock() -> Response:
    """Add a product to stock of current location then redirect back."""
    lid: str = request.json["lid"]
    pid: str = request.json["pid"]
    stock_num: str = request.json["stock"]
    ret: str = StockService.add_product_to_stock(lid, pid, stock_num)
    return make_response({"message": ret}, 200)


@stock.route(path.INCREASE_STOCK_PATH, methods=["POST"])
def increase_stock() -> Response:
    """Increase stock of a product then redirect."""
    lid: str = request.json["lid"]
    pid: str = request.json["pid"]
    ret: str = StockService.increase_stock(lid, pid)
    return make_response({"message": ret}, 200)


@stock.route(path.DECREASE_STOCK_PATH, methods=["POST"])
def decrease_stock() -> Response:
    """Decrease stock of product then redirect."""
    lid: str = request.json["lid"]
    pid: str = request.json["pid"]
    ret: str = StockService.decrease_stock(lid, pid)
    return make_response({"message": ret}, 200)


@stock.route(path.DELETE_PRODUCT_FROM_STOCK_PATH, methods=["POST"])
def delete_from_stock() -> Response:
    """Delete product from current location stock then redirect."""
    lid: str = request.json["lid"]
    pid: str = request.json["pid"]
    ret: str = StockService.delete_stock(lid, pid)
    return make_response({"message": ret}, 200)
