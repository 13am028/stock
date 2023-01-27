from db import Stock, Products, Locations, session


def find(lid: str, pid: str):
    return Stock.query.filter(Stock.location_id == lid).filter(Stock.product_id == pid).first()


def get_products(lid):
    ret = session.query(Stock, Products).join(Products).filter(Stock.location_id == lid).all()
    ret.sort(key=lambda x: x[1].product_name)
    return ret


def get_loc_name(lid):
    return Locations.query.filter(Locations.id == lid).first().location_name