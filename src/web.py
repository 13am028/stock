from flask import Blueprint, request, render_template, redirect, url_for
from utils import get_products, get_loc_name, find
from db import Stock, Products, Locations, session

web = Blueprint('web', __name__)


@web.route('/')
def index():
    return render_template('base.html')


@web.route('/locations')
def locations():
    all_locations = Locations.query.all()
    return render_template('location.html', locations=all_locations, len=len(all_locations))


@web.route('/products', methods=['GET'])
def products():
    return render_template('product.html', all_products=Products.query.all())


@web.route('/add-location', methods=['POST'])
def add_location():
    new_location = Locations(location_name=request.form["location"])
    session.add(new_location)
    session.commit()
    return redirect(url_for('web.locations'))


@web.route('/add-product', methods=['POST'])
def add_product():
    new_product = Products(product_name=request.form['product'])
    session.add(new_product)
    session.commit()
    return redirect(url_for('web.products'))


@web.route('/product-to-stock', methods=['GET', 'POST'])
def product_to_stock():
    if request.method == 'POST':
        new_product = Stock(location_id=request.form["lid"], product_id=request.form["pid"],
                            stock=request.form["stock"])
        session.add(new_product)
        session.commit()
    return stock(request.form["lid"])


@web.route('/delete-product', methods=['POST'])
def delete_product():
    pid = request.form["pid"]
    product = Products.query.filter(Products.id == pid).first()
    session.delete(product)
    session.commit()
    return render_template('product.html', all_products=Products.query.all())


@web.route('/stock/<lid>', methods=['GET'])
def stock(lid):
    all_products = Products.query.all()
    stock_products = get_products(lid)
    return render_template('stock.html', all_products=all_products, products=stock_products, lid=lid,
                           location=get_loc_name(lid))


@web.route('/increase', methods=['POST'])
def increase_stock():
    lid = request.form["lid"]
    product = find(lid, request.form["pid"])
    product.stock += 1
    session.commit()
    return redirect(url_for('web.stock', lid=lid))


@web.route('/decrease', methods=['POST'])
def decrease_stock():
    lid = request.form["lid"]
    product = find(lid, request.form["pid"])
    product.stock -= 1
    session.commit()
    return redirect(url_for('web.stock', lid=lid))


@web.route('/delete-from-stock', methods=['POST'])
def delete_from_stock():
    lid = request.form["lid"]
    product = find(lid, request.form["pid"])
    if product is not None:
        session.delete(product)
        session.commit()
    return redirect(url_for('web.stock', lid=lid))


@web.route('/edit-location/<lid>', methods=['GET'])
def edit_location(lid):
    location = Locations.query.filter(Locations.id == lid).first()
    return render_template('edit-location.html', location=location)


@web.route('/change-loc-name', methods=['POST'])
def change_loc_name():
    lid = request.form["lid"]
    Locations.query.filter(Locations.id == lid).first().location_name = request.form["location"]
    session.commit()
    return redirect(url_for('web.stock', lid=lid))


@web.route('/delete-loc', methods=['POST'])
def delete_loc():
    lid = request.form["lid"]
    loc = Locations.query.filter(Locations.id == lid).first()
    session.delete(loc)
    session.commit()
    return redirect(url_for('web.locations'))