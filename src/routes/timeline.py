from typing import List

from flask import Blueprint, Response, jsonify, make_response, request

import html_methods
from model import StockTimeline
from path import GET_TIMELINE_BY_LOCATION, GET_TIMELINE_BY_PRODUCT
from services.timeline_service import TimelineService

timeline = Blueprint("timeline", __name__)


@timeline.route(GET_TIMELINE_BY_LOCATION, methods=[html_methods.POST])
def timeline_by_lid() -> Response:
    """Add a product to stock of current location then redirect back."""
    location_id: int = request.json["location_id"]
    lid_timeline: List[StockTimeline] = TimelineService.get_timeline_by_location_id(
        location_id
    )
    ret = [stock.to_dict() for stock in lid_timeline]
    return make_response(jsonify(ret), 200)


@timeline.route(GET_TIMELINE_BY_PRODUCT, methods=[html_methods.POST])
def timeline_by_pid() -> Response:
    """Add a product to stock of current location then redirect back."""
    product_id: int = request.json["product_id"]
    pid_timeline: List[StockTimeline] = TimelineService.get_timeline_by_product_id(
        product_id
    )
    ret = [stock.to_dict() for stock in pid_timeline]
    return make_response(jsonify(ret), 200)
