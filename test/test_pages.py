from bs4 import BeautifulSoup

from app import app


def get_lid():
    html_page = app.test_client().get('/locations').data
    soup = BeautifulSoup(html_page, 'html.parser')
    line = soup.find('li').find('a').get('href')
    lid = line[line.rfind('/')+1:]
    return lid


def test_home():
    assert app.test_client().get('/').status_code == 200


def test_location():
    assert app.test_client().get('/locations').status_code == 200


def test_product():
    assert app.test_client().get('/products').status_code == 200


def test_edit_location():
    assert app.test_client().get('/edit-location/' + get_lid()).status_code == 200


def test_stock():
    assert app.test_client().get('/stock/' + get_lid()).status_code == 200
