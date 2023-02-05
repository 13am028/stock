"""Route to pages."""
from typing import List

from flask import Blueprint, render_template

from model import locations_utils, products_utils, stock_utils
from model.model import Locations, Products

page = Blueprint("page", __name__)


@page.route("/")
def index() -> str:
    """Route to home page."""
    return render_template("base.html")


@page.route("/products", methods=["GET"])
def products() -> str:
    """Route to products page."""
    return render_template(
        "product.html", all_products=products_utils.get_all_products()
    )


@page.route("/locations")
def locations() -> str:
    """Route to locations page."""
    all_locations = locations_utils.get_all_locations()
    return render_template(
        "location.html", locations=all_locations, len=len(all_locations)
    )


@page.route("/stock/<lid>", methods=["GET"])
def stock(lid: str) -> str:
    """Route to stock page."""
    all_products: List[Locations] = products_utils.get_all_products()
    stock_products: List[Products] = stock_utils.get_products(lid)
    location_name: str = locations_utils.get_loc_name(lid)
    return render_template(
        "stock.html",
        all_products=all_products,
        products=stock_products,
        lid=lid,
        location=location_name,
    )


@page.route("/edit-location/<lid>", methods=["GET"])
def edit_location(lid: str) -> str:
    """Route to edit-location page."""
    location = locations_utils.get_location(lid)
    return render_template("edit-location.html", location=location)
