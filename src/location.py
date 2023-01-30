"""Route and methods for locations."""
from flask import Blueprint, redirect, request, url_for
from werkzeug import Response

from db import Locations, session

location = Blueprint("location", __name__)


@location.route("/add-location", methods=["POST"])
def add_location() -> Response:
    """Add new location and redirect to /locations."""
    new_location: Locations = Locations(location_name=request.form["location"])
    session.add(new_location)
    session.commit()
    return redirect(url_for("page.locations"))


@location.route("/change-loc-name", methods=["POST"])
def change_loc_name() -> Response:
    """Change location name and redirect to /stock."""
    lid: str = request.form["lid"]
    Locations.query.filter(Locations.id == lid).first().location_name = request.form["location"]
    session.commit()
    return redirect(url_for("page.stock", lid=lid))


@location.route("/delete-loc", methods=["POST"])
def delete_loc() -> Response:
    """Delete location and redirect to /locations."""
    lid: str = request.form["lid"]
    loc: Locations = Locations.query.filter(Locations.id == lid).first()
    session.delete(loc)
    session.commit()
    return redirect(url_for("page.locations"))
