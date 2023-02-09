"""Database."""
import datetime
from typing import Dict

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, ForeignKey

db = SQLAlchemy()
session = db.session


class Locations(db.Model):
    """Location Model."""

    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(length=100), unique=True, nullable=False)

    def to_dict(self) -> Dict:
        """Convert Locations to Dict."""
        return {"id": self.id, "location_name": self.location_name}


class Products(db.Model):
    """Product Model."""

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(length=100), unique=True, nullable=False)

    def to_dict(self) -> Dict:
        """Convert Products to Dict."""
        return {"id": self.id, "product_name": self.product_name}


class Stock(db.Model):
    """Stock Model."""

    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, ForeignKey(Locations.id, ondelete="CASCADE"))
    product_id = db.Column(db.Integer, ForeignKey(Products.id, ondelete="CASCADE"))
    stock = db.Column(db.Integer)

    def to_dict(self) -> Dict:
        """Convert Stock to Dict."""
        return {
            "id": self.id,
            "location_id": self.location_id,
            "product_id": self.product_id,
            "stock": self.stock,
        }


class StockTimeline(db.Model):
    """Stock Timeline Model."""

    __tablename__ = "timeline"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, ForeignKey(Locations.id, ondelete="CASCADE"))
    product_id = db.Column(db.Integer, ForeignKey(Products.id, ondelete="CASCADE"))
    all_products = db.Column(db.ARRAY(db.Integer))
    stock = db.Column(db.Integer)
    date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, location_id: int, product_id: int, stock: int) -> None:
        """Initialize new StockTimeline Object."""
        self.location_id = location_id
        self.product_id = product_id
        self.stock = stock
        all_product = [
            product.id
            for product in Stock.query.filter_by(location_id=location_id).all()
        ]
        all_product.append(product_id)
        self.all_products = all_product
        self.date = datetime.datetime.utcnow()

    def get_all_product_stock(self) -> Dict:
        """Get all product names and their stocks in StockTimeline.all_products."""
        ret = {}
        for product_id in self.all_products:
            if product_id == self.product_id:
                ret[self.product_id] = {
                    "product_name": Products.query.filter_by(id=self.product_id)
                    .first()
                    .product_name,
                    "stock": self.stock,
                }
                continue
            timeline = (
                StockTimeline.query.filter(StockTimeline.date < self.date)
                .filter_by(product_id=product_id)
                .all()
            )
            if len(timeline) > 0:
                product = timeline[-1]
                ret[product.product_id] = {
                    "product_name": Products.query.filter_by(id=product.product_id)
                    .first()
                    .product_name,
                    "stock": product.stock,
                }
        return ret

    def to_dict(self) -> Dict:
        """Return dict of timeline."""
        return {
            "id": self.id,
            "location_name": Locations.query.filter(Locations.id == self.location_id)
            .first()
            .location_name,
            "product_name": Products.query.filter(Products.id == self.product_id)
            .first()
            .product_name,
            "all_products": self.get_all_product_stock(),
            "stock": self.stock,
            "time": str(self.date),
        }
