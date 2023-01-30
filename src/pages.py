"""Route to pages."""
from typing import List

from flask import Blueprint, render_template

from db import Locations, Products
from utils import get_loc_name, get_products

page = Blueprint("page", __name__)


@page.route("/")
def index() -> str:
    """Route to home page."""
    return render_template("base.html")


@page.route("/products", methods=["GET"])
def products() -> str:
    """Route to products page."""
    return render_template("product.html", all_products=Products.query.all())


@page.route("/locations")
def locations() -> str:
    """Route to locations page."""
    all_locations: List[Locations] = Locations.query.all()
    return render_template(
        "location.html", locations=all_locations, len=len(all_locations)
    )


@page.route("/stock/<lid>", methods=["GET"])
def stock(lid: str) -> str:
    """Route to stock page."""
    all_products: List[Locations] = Products.query.all()
    stock_products: List[Products] = get_products(lid)
    return render_template(
        "stock.html",
        all_products=all_products,
        products=stock_products,
        lid=lid,
        location=get_loc_name(lid),
    )


@page.route("/edit-location/<lid>", methods=["GET"])
def edit_location(lid: str) -> str:
    """Route to edit-location page."""
    location: List[Locations] = Locations.query.filter(Locations.id == lid).first()
    return render_template("edit-location.html", location=location)
