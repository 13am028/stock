"""Route and methods for locations."""
from typing import Dict

from flask import Blueprint, make_response, request
from werkzeug import Response

import html_methods
from services.locations_service import LocationService
from path import ADD_LOCATION_PATH, CHANGE_LOCATION_NAME_PATH, DELETE_LOCATION_PATH

location = Blueprint("location", __name__)


@location.route(ADD_LOCATION_PATH, methods=[html_methods.POST])
def add_location() -> Response:
    """Add new location and redirect to /locations."""
    location_name: str = request.json["location_name"]
    ret: Dict = LocationService.add_location(location_name).to_dict()
    return make_response(ret, 200)


@location.route(CHANGE_LOCATION_NAME_PATH, methods=[html_methods.PUT])
def change_location_name() -> Response:
    """Change location name and redirect to /stock."""
    location_id: int = request.json["location_id"]
    location_name: str = request.json["location_name"]
    ret: Dict = LocationService.change_location_name(
        location_id, location_name
    ).to_dict()
    return make_response(ret, 200)


@location.route(DELETE_LOCATION_PATH, methods=[html_methods.DELETE])
def delete_location() -> Response:
    """Delete location and redirect to /locations."""
    location_id: int = request.json["location_id"]
    ret: Dict = LocationService.delete_location(location_id).to_dict()
    return make_response(ret, 200)
