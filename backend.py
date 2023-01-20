import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy_utils import create_database, database_exists

# url = "postgresql://" + os.environ["POSTGRES_USER"] + ":" + os.environ[
#     "POSTGRES_PASSWORD"] + "@" + os.environ["POSTGRES_DB"] + "/stock"
url = "postgresql://" + "dbc" ":" + "dbc" + "@" + "localhost:5434" + "/stock"
if not database_exists(url):
    create_database(url)

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = url
db = SQLAlchemy(app)


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


db.create_all()
session = db.session


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/locations')
def locations():
    all_locations = Locations.query.all()
    return render_template('location.html', locations=all_locations, len=len(all_locations))


@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        new_product = Products(product_name=request.form['product'])
        session.add(new_product)
        session.commit()
    return render_template('product.html', all_products=Products.query.all())


@app.route('/add-location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        new_location = Locations(location_name=request.form["location"])
        session.add(new_location)
        session.commit()
    return locations()


@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = Stock(location_id=request.form["lid"], product_id=request.form["pid"],
                            stock=request.form["stock"])
        session.add(new_product)
        session.commit()
    return stock(request.form["lid"])


@app.route('/delete-product', methods=['POST'])
def delete_product():
    pid = request.form["pid"]
    product = Products.query.filter(Products.id == pid).first()
    session.delete(product)
    session.commit()
    return render_template('product.html', all_products=Products.query.all())


def find(lid: str, pid: str):
    return Stock.query.filter(Stock.location_id == lid).filter(Stock.product_id == pid).first()


@app.route('/stock/<lid>', methods=['GET'])
def stock(lid):
    all_products = Products.query.all()
    products = get_products(lid)
    return render_template('stock.html', all_products=all_products, products=products, lid=lid,
                           location=get_loc_name(lid))


@app.route('/increase', methods=['POST'])
def increase_stock():
    lid = request.form["lid"]
    product = find(lid, request.form["pid"])
    product.stock += 1
    session.commit()
    return stock(lid)


@app.route('/decrease', methods=['POST'])
def decrease_stock():
    lid = request.form["lid"]
    product = find(lid, request.form["pid"])
    product.stock -= 1
    session.commit()
    return stock(lid)


@app.route('/delete-from-stock', methods=['POST'])
def delete_from_stock():
    lid = request.form["lid"]
    product = find(lid, request.form["pid"])
    if product is not None:
        session.delete(product)
        session.commit()
    return stock(lid)


@app.route('/edit-location/<lid>', methods=['GET'])
def edit_location(lid):
    location = Locations.query.filter(Locations.id == lid).first()
    return render_template('edit-location.html', location=location)


@app.route('/change_loc_name', methods=['POST'])
def change_loc_name():
    lid = request.form["lid"]
    Locations.query.filter(Locations.id == lid).first().location_name = request.form["location"]
    session.commit()
    return stock(lid)


@app.route('/delete_loc', methods=['POST'])
def delete_loc():
    lid = request.form["lid"]
    loc = Locations.query.filter(Locations.id == lid).first()
    session.delete(loc)
    session.commit()
    return locations()


def get_products(lid):
    ret = session.query(Stock, Products).join(Products).filter(Stock.location_id == lid).all()
    ret.sort(key=lambda x: x[1].product_name)
    return ret


def get_loc_name(lid):
    return Locations.query.filter(Locations.id == lid).first().location_name


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=7777)
