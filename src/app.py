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

# url = (
#     "postgresql://"
#     + os.environ["POSTGRES_USER"]
#     + ":"
#     + os.environ["POSTGRES_PASSWORD"]
#     + "@"
#     + os.environ["POSTGRES_DB"]
#     + "/stock"
# )

url = "postgresql://" + "dbc" ":" + "dbc" + "@" + "localhost:5434" + "/stock"


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


"""Register blueprints to app."""
app.register_blueprint(page)
app.register_blueprint(location)
app.register_blueprint(product)
app.register_blueprint(stock)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=7778)
