"""Create and serve app."""
import os

import flask.app
from flask import Flask
from sqlalchemy_utils import create_database, database_exists
from waitress import serve

from db import db
from location import location
from pages import page
from product import product
from stock import stock

url = (
    "postgresql://"
    + os.environ["POSTGRES_USER"]
    + ":"
    + os.environ["POSTGRES_PASSWORD"]
    + "@"
    + os.environ["POSTGRES_DB"]
    + "/stock"
)


def create_db() -> None:
    """Create database tables if not exist."""
    if not database_exists(url):
        create_database(url)


def create_app() -> flask.app.Flask:
    """Create Flask app."""
    app: flask.app.Flask = Flask(__name__)
    app.app_context().push()
    app.config["SQLALCHEMY_DATABASE_URI"] = url
    return app


def init_app_db(app: flask.app.Flask) -> None:
    """Initiate database to app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()


def register_blueprint(app: flask.app.Flask) -> None:
    """Register blueprints to app."""
    app.register_blueprint(page)
    app.register_blueprint(location)
    app.register_blueprint(product)
    app.register_blueprint(stock)


def serve_app(app: flask.app.Flask) -> None:
    """Serve the app using waitress."""
    serve(app, host="0.0.0.0", port=7777)


if __name__ == "__main__":
    create_db()
    app: flask.app.Flask = create_app()
    print(type(app))
    init_app_db(app)
    register_blueprint(app)
    serve_app(app)
