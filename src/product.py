"""Route and methods for products."""
from flask import Blueprint, Response, redirect, request, url_for

from db import Products, session

product = Blueprint("product", __name__)


@product.route("/add-product", methods=["POST"])
def add_product() -> Response:
    """Add a new product."""
    new_product: Products = Products(product_name=request.form["product"])
    session.add(new_product)
    session.commit()
    return redirect(url_for("page.products"))


@product.route("/delete-product", methods=["POST"])
def delete_product() -> Response:
    """Delete product."""
    pid: str = request.form["pid"]
    del_product = Products.query.filter(Products.id == pid).first()
    session.delete(del_product)
    session.commit()
    return redirect(url_for("page.products"))
