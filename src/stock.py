"""Route and methods for stock."""
from flask import (Blueprint, Response, make_response, redirect, request,
                   url_for)

from db import Products, Stock, session
from utils import find

stock = Blueprint("stock", __name__)
stock_page = "page.stock"


@stock.route("/product-to-stock", methods=["POST"])
def product_to_stock() -> Response:
    """Add a product to stock of current location then redirect back."""
    lid: str = request.form["lid"]
    pid: str = request.form["pid"]
    stock_num: str = request.form["stock"]
    new_stock: Stock = Stock(location_id=lid, product_id=pid, stock=stock_num)
    if int(request.form["stock"]) < 0:
        return make_response("Product Not Found !")
    session.add(new_stock)
    session.commit()
    return redirect(url_for(stock_page, lid=lid))


@stock.route("/increase", methods=["PUT"])
def increase_stock() -> Response:
    """Increase stock of a product then redirect."""
    lid: str = request.form["lid"]
    product: Products = find(lid, request.form["pid"])
    if product is None:
        return make_response("Product Not Found !")
    product.stock += 1
    session.commit()
    return redirect(url_for(stock_page, lid=lid))


@stock.route("/decrease", methods=["PUT"])
def decrease_stock() -> Response:
    """Decrease stock of product then redirect."""
    lid: str = request.form["lid"]
    product: Products = find(lid, request.form["pid"])
    if product is None:
        return make_response("Product Not Found !")
    if product.stock > 0:
        product.stock -= 1
        session.commit()
    return redirect(url_for(stock_page, lid=lid))


@stock.route("/delete-from-stock", methods=["DELETE"])
def delete_from_stock() -> Response:
    """Delete product from current location stock then redirect."""
    lid: str = request.form["lid"]
    product: Products = find(lid, request.form["pid"])
    if product is None:
        return make_response("Product Not Found !")
    session.delete(product)
    session.commit()
    return redirect(url_for(stock_page, lid=lid))