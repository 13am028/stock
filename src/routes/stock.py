"""Route and methods for stock."""
from flask import Blueprint, Response, redirect, request, url_for

from model import stock_utils

stock = Blueprint("stock", __name__)
stock_page = "page.stock"

product_not_found = {"message": "Product Not Found !"}


@stock.route("/product-to-stock", methods=["POST"])
def product_to_stock() -> Response:
    """Add a product to stock of current location then redirect back."""
    lid: str = request.form["lid"]
    pid: str = request.form["pid"]
    stock_num: str = request.form["stock"]
    stock_utils.product_to_stock(lid, pid, stock_num)
    return redirect(url_for(stock_page, lid=lid))


@stock.route("/increase", methods=["POST"])
def increase_stock() -> Response:
    """Increase stock of a product then redirect."""
    lid: str = request.form["lid"]
    pid: str = request.form["pid"]
    stock_utils.increase_stock(lid, pid)
    return redirect(url_for(stock_page, lid=lid))


@stock.route("/decrease", methods=["POST"])
def decrease_stock() -> Response:
    """Decrease stock of product then redirect."""
    lid: str = request.form["lid"]
    pid: str = request.form["pid"]
    stock_utils.decrease_stock(lid, pid)
    return redirect(url_for(stock_page, lid=lid))


@stock.route("/delete-from-stock", methods=["POST"])
def delete_from_stock() -> Response:
    """Delete product from current location stock then redirect."""
    lid: str = request.form["lid"]
    pid: str = request.form["pid"]
    stock_utils.delete_stock(lid, pid)
    return redirect(url_for(stock_page, lid=lid))
