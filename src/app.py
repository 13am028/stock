"""Create and serve app."""
import os

import flask.app
from flask import Flask
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import create_database, database_exists
from waitress import serve

from model import db
from routes.location import location
from routes.pages import page
from routes.product import product
from routes.stock import stock
from routes.timeline import timeline
from services.locations_service import LocationService
from services.products_service import ProductService
from services.stock_service import StockService

url = (
    "postgresql://"
    + os.environ["POSTGRES_USER"]
    + ":"
    + os.environ["POSTGRES_PASSWORD"]
    + "@"
    + os.environ["POSTGRES_DB"]
    + "/stock"
)


"""Create database tables if not exist."""
if not database_exists(url):
    create_database(url)


"""Create Flask app."""
app: flask.app.Flask = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = url


"""Initiate database to app."""
db.init_app(app)
with app.app_context():
    db.create_all()
    db.session.commit()
    try:
        LocationService.add_location("test location")
        ProductService.add_product("test product")
        StockService.add_product_to_stock(1, 1, 1)
    except SQLAlchemyError:
        pass


"""Register blueprints to app."""
app.register_blueprint(page)
app.register_blueprint(location)
app.register_blueprint(product)
app.register_blueprint(stock)
app.register_blueprint(timeline)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=7777)
