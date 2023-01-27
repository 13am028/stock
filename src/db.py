from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(length=100), unique=True, nullable=False)


class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(length=100), unique=True, nullable=False)


class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, ForeignKey(Locations.id, ondelete='CASCADE'))
    product_id = db.Column(db.Integer, ForeignKey(Products.id, ondelete='CASCADE'), unique=True)
    stock = db.Column(db.Integer)


session = db.session
