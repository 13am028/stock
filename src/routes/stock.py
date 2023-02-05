"""Route and methods for stock."""
from flask import Blueprint, Response, make_response, request

from model import stock_utils

stock = Blueprint("stock", __name__)
stock_page = "page.stock"

product_not_found = {"message": "Product Not Found !"}


@stock.route("/product-to-stock", methods=["POST"])
def product_to_stock() -> Response:
    """Add a product to stock of current location then redirect back."""
    lid: str = request.json["lid"]
    pid: str = request.json["pid"]
    stock_num: str = request.json["stock"]
    ret: str = stock_utils.product_to_stock(lid, pid, stock_num)
    return make_response(ret, 200)


@stock.route("/increase", methods=["POST"])
def increase_stock() -> Response:
    """Increase stock of a product then redirect."""
    lid: str = request.json["lid"]
    pid: str = request.json["pid"]
    ret: str = stock_utils.increase_stock(lid, pid)
    return make_response(ret, 200)


@stock.route("/decrease", methods=["POST"])
def decrease_stock() -> Response:
    """Decrease stock of product then redirect."""
    lid: str = request.json["lid"]
    pid: str = request.json["pid"]
    ret: str = stock_utils.decrease_stock(lid, pid)
    return make_response(ret, 200)


@stock.route("/delete-from-stock", methods=["POST"])
def delete_from_stock() -> Response:
    """Delete product from current location stock then redirect."""
    lid: str = request.json["lid"]
    pid: str = request.json["pid"]
    ret: str = stock_utils.delete_stock(lid, pid)
    return make_response(ret, 200)
