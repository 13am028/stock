"""Database."""
import datetime
from typing import Dict

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, ForeignKey

db = SQLAlchemy()


class Locations(db.Model):
    """Location Model."""

    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(length=100), unique=True, nullable=False)


class Products(db.Model):
    """Product Model."""

    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(length=100), unique=True, nullable=False)


class Stock(db.Model):
    """Stock Model."""

    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, ForeignKey(Locations.id, ondelete="CASCADE"))
    product_id = db.Column(
        db.Integer, ForeignKey(Products.id, ondelete="CASCADE"), unique=True
    )
    stock = db.Column(db.Integer)


class StockTimeline(db.Model):
    """Stock Timeline Model."""

    __tablename__ = "timeline"
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, ForeignKey(Locations.id, ondelete="CASCADE"))
    product_id = db.Column(db.Integer, ForeignKey(Products.id, ondelete="CASCADE"))
    stock = db.Column(db.Integer)
    date = db.Column(DateTime, default=datetime.datetime.utcnow)

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
            "stock": self.stock,
            "time": str(self.date),
        }
