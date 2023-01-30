"""Utility functions."""
from typing import Any, List

from db import Locations, Products, Stock, session


def find(lid: str, pid: str) -> Stock:
    """Find the product with given location id and product id."""
    return (
        Stock.query.filter(Stock.location_id == lid)
        .filter(Stock.product_id == pid)
        .first()
    )


def get_products(lid: str) -> List[Any]:
    """Get all products given location id."""
    ret: List[Any] = (
        session.query(Stock, Products)
        .join(Products)
        .filter(Stock.location_id == lid)
        .all()
    )
    ret.sort(key=lambda x: x[1].product_name)
    return ret


def get_loc_name(lid: str) -> str:
    """Get the location name give location id."""
    return Locations.query.filter(Locations.id == lid).first().location_name
