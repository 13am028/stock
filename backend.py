import os

from flask import request, Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import ForeignKey

# url = "postgresql://" + os.environ["POSTGRES_USER"] + ":" + os.environ[
#     "POSTGRES_PASSWORD"] + "@" + os.environ["POSTGRES_DB"] + "/stock"
url = "postgresql://" + "dbc" ":" + "dbc" + "@" + "localhost:5434" + "/stock"
if not database_exists(url):
    create_database(url)

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = url
db = SQLAlchemy(app)


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(length=100), unique=True, nullable=False)


class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, ForeignKey(Location.id))
    product_id = db.Column(db.String(length=50), unique=True, nullable=False)
    product_name = db.Column(db.String(length=100), nullable=False)
    stock = db.Column(db.Integer)


db.create_all()
session = db.session


def to_dict(row):
    ret = row.__dict__
    ret.pop("_sa_instance_state")
    return ret


@app.route('/')
def index():
    return make_response({"message": "Welcome to Vending Machine Tracking Application !"}, 200)


@app.route('/all-location', methods=['GET'])
def all_loc():
    locations = [to_dict(loc) for loc in Location.query.all()]
    return make_response(locations, 200)


@app.route('/stock', methods=['GET'])
def stock():
    lid = request.form["lid"]
    all_products = get_all_products(lid)
    return make_response(all_products, 200)


@app.route('/add-location', methods=['POST'])
def add_location():
    if request.method == 'POST':
        new_location = Location(location_name=request.form["location"])
        session.add(new_location)
        session.commit()
    return make_response({"message": "New location added !"}, 200)


@app.route('/add-product', methods=['POST'])
def add_product():
    new_product = Stock(location_id=request.form["lid"], product_id=request.form["pid"],
                        product_name=request.form["name"], stock=request.form["stock"])
    session.add(new_product)
    session.commit()
    return make_response("New product added !", 200)


def find(lid: str, pid: str):
    return Stock.query.filter(Stock.location_id == lid).filter(Stock.product_id == pid).first()


@app.route('/increase', methods=['POST'])
def increase_stock():
    lid = request.form["lid"]
    product = find(lid, request.form["pid"])
    product.stock += 1
    session.commit()
    return make_response({"stock": product.stock}, 200)


@app.route('/decrease', methods=['POST'])
def decrease_stock():
    lid = request.form["lid"]
    product = find(lid, request.form["pid"])
    product.stock -= 1
    session.commit()
    return make_response({"stock": product.stock}, 200)


@app.route('/delete', methods=['POST'])
def delete_product():
    lid = request.form["lid"]
    product = find(lid, request.form["pid"])
    if product is not None:
        session.delete(product)
        session.commit()
    return make_response({"message": "Product successfully deleted !"}, 200)


@app.route('/change-loc-name', methods=['POST'])
def change_loc_name():
    lid = request.form["lid"]
    loc = Location.query.filter(Location.id == lid).first()
    loc.location_name = request.form["location"]
    session.commit()
    return make_response(loc.location_name, 200)


@app.route('/delete-loc', methods=['POST'])
def delete_loc():
    lid = request.form["lid"]
    loc = Location.query.filter(Location.id == lid).first()
    session.delete(loc)
    session.commit()
    return make_response({"message": "Location successfully deleted !"}, 200)


def get_all_products(lid):
    ret = [to_dict(item) for item in Stock.query.filter(Stock.location_id == lid).all()]
    return make_response(ret, 200)


def get_location(lid):
    return Location.query.filter(Location.id == lid).first().location_name


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=7777)
