"""Route to pages."""
from typing import List

from flask import Blueprint, render_template

import html_methods
import path
from model.locations_service import LocationService
from model.model import Locations, Products
from model.products_service import ProductService
from model.stock_service import StockService

page = Blueprint("page", __name__)


@page.route("/")
def index() -> str:
    """Route to home page."""
    return render_template(path.BASE_TEMPLATE)


@page.route(path.ALL_PRODUCTS_PATH, methods=[html_methods.GET])
def products() -> str:
    """Route to products page."""
    return render_template(
        path.PRODUCT_TEMPLATE, all_products=ProductService.get_all_products()
    )


@page.route(path.ALL_LOCATIONS_PATH, methods=[html_methods.GET])
def locations() -> str:
    """Route to locations page."""
    all_locations = LocationService.get_all_locations()
    return render_template(
        path.LOCATION_TEMPLATE, locations=all_locations, len=len(all_locations)
    )


@page.route(path.STOCK_DETAIL_PATH, methods=[html_methods.GET])
def stock(location_id: int) -> str:
    """Route to stock page."""
    all_products: List[Locations] = ProductService.get_all_products()
    stock_products: List[Products] = StockService.get_products(location_id)
    location_name: str = LocationService.get_location_name(location_id)
    return render_template(
        path.STOCK_TEMPLATE,
        all_products=all_products,
        products=stock_products,
        lid=location_id,
        location=location_name,
    )


@page.route(path.EDIT_LOCATION_PATH, methods=[html_methods.GET])
def edit_location(location_id: int) -> str:
    """Route to edit-location page."""
    location = LocationService.get_location(location_id)
    return render_template(path.EDIT_LOCATION_TEMPLATE, location=location)


@page.route(path.STOCK_TIMELINE_PATH, methods=[html_methods.GET])
def timeline() -> str:
    """Route to edit-location page."""
    all_locations = LocationService.get_all_locations()
    all_products = ProductService.get_all_products()
    return render_template(
        path.TIMELINE_TEMPLATE, locations=all_locations, products=all_products
    )
