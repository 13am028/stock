"""Route and methods for locations."""
from flask import Blueprint, make_response, request
from werkzeug import Response

from model import locations_utils

location = Blueprint("location", __name__)


@location.route("/add-location", methods=["POST"])
def add_location() -> Response:
    """Add new location and redirect to /locations."""
    location_name = request.json["location"]
    ret: str = locations_utils.add_loc(location_name)
    return make_response(ret, 200)


@location.route("/change-loc-name", methods=["POST"])
def change_loc_name() -> Response:
    """Change location name and redirect to /stock."""
    lid: str = request.json["lid"]
    location_name: str = request.json["location"]
    ret: str = locations_utils.change_loc_name(lid, location_name)
    return make_response(ret, 200)


@location.route("/delete-loc", methods=["POST"])
def delete_loc() -> Response:
    """Delete location and redirect to /locations."""
    lid: str = request.json["lid"]
    ret: str = locations_utils.delete_loc(lid)
    return make_response(ret, 200)
