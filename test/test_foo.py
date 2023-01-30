import string
import random

from bs4 import BeautifulSoup
from app import app


def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return result_str


def test_add_location():
    loc_name = get_random_string(7)
    app.test_client().post('/add-location', data={'location': loc_name})

    html_page = app.test_client().get('/locations').data
    soup = BeautifulSoup(html_page, 'html.parser')
    locations = []
    for name in soup.findAll('a'):
        locations.append(name.getText())
    assert loc_name in locations


def test_add_product():
    product_name = get_random_string(7)
    app.test_client().post('/add-product', data={'product': product_name})

    html_page = app.test_client().get('/products').data
    soup = BeautifulSoup(html_page, 'html.parser')
    products = []
    for name in soup.findAll('h3'):
        products.append(name.getText())
    assert product_name in products



# def test_index():
#     res = app.test_client().get('/')
#     assert res.status_code == 200


# def test_add_loc():
#     res = app.test_client().post('/add-location', data={
#         'location': 'MUIC'
#     })
#     assert res.status_code == 200
#
#
# def test_new_product():
#     res = app.test_client().post('/products', data={
#         'product': 'Coke'
#     })
#     assert res.status_code == 200
#
#
# def test_locations():
#     res = app.test_client().get('/locations')
#     assert res.status_code == 200
#
#
# def test_products():
#     res = app.test_client().get('/products')
#     assert res.status_code == 200
#
#
# def test_add_product():
#     res = app.test_client().post('/add-product', data={
#         'lid': 2,
#         'pid': 7,
#         'stock': 1,
#     })
#     assert res.status_code == 200
#
#
# def test_stock():
#     res = app.test_client().get('/stock/2')
#     assert res.status_code == 200
#
#
# def test_increase_stock():
#     res = app.test_client().post('/increase',  data={
#         'lid': 2,
#         'pid': 7,
#     })
#     assert res.status_code == 200
#
#
# def test_decrease_stock():
#     res = app.test_client().post('/increase',  data={
#         'lid': 2,
#         'pid': 7,
#     })
#     assert res.status_code == 200
#
#
# def test_delete_from_stock():
#     res = app.test_client().post('/delete-from-stock',  data={
#         'lid': 2,
#         'pid': 7,
#     })
#     assert res.status_code == 200
#
#
# def test_edit_location():
#     res = app.test_client().get('/edit-location')
#     assert res.status_code == 200
#
#
# def test_change_loc_name():
#     res = app.test_client().post('/change_loc_name', data={
#         'lid': 2,
#         'location': 'Muic'
#     })
#     assert res.status_code == 200
#
#
# def test_delete_product():
#     res = app.test_client().post('/delete-product', data={
#         'pid': 7
#     })
#     assert res.status_code == 200
#
#
# def test_delete_loc():
#     res = app.test_client().post('/delete_loc', data={
#         'lid': 2
#     })
#     assert res.status_code == 200

