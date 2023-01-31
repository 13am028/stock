import random
import string

from bs4 import BeautifulSoup

from app import app

location_uri = '/locations'
parser = 'html.parser'


def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_letters) for _ in range(length))
    return result_str


def get_lid():
    html_page = app.test_client().get(location_uri).data
    soup = BeautifulSoup(html_page, parser)
    line = soup.find('li').find('a').get('href')
    lid = line[line.rfind('/')+1:]
    return lid


def test_add_location():
    loc_name = get_random_string(7)
    app.test_client().post('/add-location', data={'location': loc_name})

    html_page = app.test_client().get(location_uri).data
    soup = BeautifulSoup(html_page, parser)
    assert loc_name == soup.find(text=loc_name)


def test_change_loc_name():
    lid = get_lid()
    rand_name = get_random_string(7)
    app.test_client().post('/change-loc-name', data={'lid': lid, 'location': rand_name})
    html_page = app.test_client().get('/stock/' + lid).data
    soup = BeautifulSoup(html_page, parser)
    loc_name = ''
    for text in soup.find_all('h2'):
        if 'Location' in text.getText():
            loc_name = text.getText().split()[-1]

    assert rand_name == loc_name


def test_delete_loc():
    lid = get_lid()
    app.test_client().post('/delete-loc', data={'lid': lid})
    html_page = app.test_client().get(location_uri).data
    soup = BeautifulSoup(html_page, parser)
    found = False
    for tag in soup.findAll('a'):
        text = tag.get('href')
        if text[text.rfind('/')+1:] == lid:
            found = True
    assert found is False
