import os

from flask import request, Flask, render_template
from flask_sqlalchemy import SQLAlchemy
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


class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(length=100))


class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.String(length=50))
    product_id = db.Column(db.String(length=50))
    product_name = db.Column(db.String(length=100))
    stock = db.Column(db.Integer)


db.create_all()
session = db.session


@app.route('/')
def index():
    all_locations = Location.query.all()
    return render_template('location.html', locations=all_locations, len=len(all_locations))


@app.route('/stock/<lid>', methods=['GET'])
def stock(lid):
    all_products = get_all_products(lid)
    return render_template('stock.html', all_products=all_products, len=len(all_products), lid=lid, location=get_location(lid))


@app.route('/add-location', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        new_location = Location(location_name=request.form["location"])
        session.add(new_location)
        session.commit()
    return index()


@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        new_product = Stock(location_id=request.form["lid"], product_id=request.form["pid"], product_name=request.form["name"], stock=request.form["stock"])
        session.add(new_product)
        session.commit()
    return stock(request.form["lid"])


def find(lid: str, pid: str):
    return Stock.query.filter(Stock.location_id==lid).filter(Stock.product_id==pid).first()


@app.route('/increase', methods=['POST'])
def increase_stock():
    lid = request.form["location"]
    product = find(lid, request.form["product"])
    product.stock += 1
    session.commit()
    return stock(lid)


@app.route('/decrease', methods=['POST'])
def decrease_stock():
    lid = request.form["location"]
    product = find(lid, request.form["product"])
    product.stock -= 1
    session.commit()
    return stock(lid)


@app.route('/delete', methods=['POST'])
def delete_product():
    lid = request.form["location"]
    product = find(lid, request.form["product"])
    if product is not None:
        session.delete(product)
        session.commit()
    return stock(lid)


@app.route('/edit-location/<lid>', methods=['GET'])
def edit_location(lid):
    location = Location.query.filter(Location.id==lid).first()
    return render_template('edit-location.html', location=location)


@app.route('/change_loc_name', methods=['POST'])
def change_loc_name():
    lid = request.form["lid"]
    Location.query.filter(Location.id==lid).first().location_name = request.form["location"]
    session.commit()
    return stock(lid)


@app.route('/delete_loc', methods=['POST'])
def delete_loc():
    lid = request.form["lid"]
    loc = Location.query.filter(Location.id==lid).first()
    session.delete(loc)
    session.commit()
    return index()


def get_all_products(lid):
    ret = Stock.query.filter(Stock.location_id==lid).all()
    ret.sort(key=lambda x: x.product_name)
    return ret


def get_location(lid):
    return Location.query.filter(Location.id==lid).first().location_name


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=7777)
