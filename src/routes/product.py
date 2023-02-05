"""Route and methods for products."""
from flask import Blueprint, Response, redirect, request, url_for

from model import products_utils

product = Blueprint("product", __name__)


@product.route("/add-product", methods=["POST"])
def add_product() -> Response:
    """Add a new product."""
    product_name = request.form["product"]
    products_utils.add_product(product_name)
    return redirect(url_for("page.products"))


@product.route("/delete-product", methods=["POST"])
def delete_product() -> Response:
    """Delete product."""
    pid: str = request.form["pid"]
    products_utils.delete_product(pid)
    return redirect(url_for("page.products"))
