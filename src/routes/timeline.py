from typing import List

from flask import Blueprint, Response, make_response, request

from model.model import StockTimeline
from model.timeline_service import TimelineService
from path import GET_TIMELINE_BY_LOCATION, GET_TIMELINE_BY_PRODUCT

timeline = Blueprint("timeline", __name__)


@timeline.route(GET_TIMELINE_BY_LOCATION, methods=["POST"])
def timeline_by_lid() -> Response:
    """Add a product to stock of current location then redirect back."""
    lid: str = request.json["lid"]
    lid_timeline: List[StockTimeline] = TimelineService.get_timeline_by_location_id(lid)
    ret = [stock.to_dict() for stock in lid_timeline]
    return make_response({"timeline": ret}, 200)


@timeline.route(GET_TIMELINE_BY_PRODUCT, methods=["POST"])
def timeline_by_pid() -> Response:
    """Add a product to stock of current location then redirect back."""
    pid: str = request.json["pid"]
    pid_timeline: List[StockTimeline] = TimelineService.get_timeline_by_product_id(pid)
    ret = [stock.to_dict() for stock in pid_timeline]
    return make_response({"timeline": ret}, 200)
