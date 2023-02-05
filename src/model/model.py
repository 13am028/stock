"""Database."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()
session = db.session


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


def session_commit() -> str:
    """Try session.commit(), return Success/Database Failure."""
    try:
        session.commit()
    except SQLAlchemyError:
        return "Database Failure"
    return "Success"
