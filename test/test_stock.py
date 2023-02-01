from bs4 import BeautifulSoup
from flask.json import tag

from app import app

product_not_found = "Product Not Found !"
stock_uri = '/stock/'
parser = 'html.parser'


def get_lid() -> str:
    """Get the first location_id found."""
    html_page: str = app.test_client().get("/locations").data
    soup = BeautifulSoup(html_page, parser)
    line: str = soup.find("li").find("a").get("href")
    lid: str = line[line.rfind("/") + 1 :]
    return lid


def get_pid() -> str:
    """Get the first product_id found."""
    html_page: str = app.test_client().get("/products").data
    soup = BeautifulSoup(html_page, "html.parser")
    pid: str = soup.find("input", {"name": "pid"}).get("value")
    return pid


def get_stock(lid: str, pid: str) -> int:
    html_page = app.test_client().get(stock_uri + lid).data
    soup = BeautifulSoup(html_page, parser)
    stock = soup.find('div', {'id': pid}).find('h4').getText().split()[-1]
    return int(stock)


def get_product(lid: str, pid: str) -> tag:
    html_page = app.test_client().get(stock_uri + lid).data
    soup = BeautifulSoup(html_page, parser)
    return soup.find('div', {'id': pid})


def test_product_to_stock():
    """Test adding product to stock."""
    uri = "/product-to-stock"
    lid = get_lid()
    pid = get_pid()
    res_success = app.test_client().post(
        uri, data={"lid": lid, "pid": pid, "stock": 10}
    )
    assert res_success.status_code == 302
    assert get_product(lid, pid) is not None
    res_fail = app.test_client().post(
        uri, data={"lid": -1, "pid": -1, "stock": -1}
    )
    assert res_fail.json["message"] == "Stock Cannot Be Negative !"
    res_duplicate = app.test_client().post(
        uri, data={"lid": lid, "pid": pid, "stock": 100}
    )
    assert res_duplicate.status_code == 302


def test_increase_stock():
    """Test increasing stock."""
    lid = get_lid()
    pid = get_pid()
    stock = get_stock(lid, pid)
    res = app.test_client().post("/increase", data={"lid": lid, "pid": pid})
    assert res.status_code == 302
    assert stock + 1 == get_stock(lid, pid)
    res = app.test_client().post("/increase", data={"lid": -1, "pid": -1})
    assert res.json["message"] == product_not_found


def test_decrease_stock():
    """Test decreasing stock."""
    lid = get_lid()
    pid = get_pid()
    stock = get_stock(lid, pid)
    res = app.test_client().post("/decrease", data={"lid": lid, "pid": pid})
    assert res.status_code == 302
    assert stock - 1 == get_stock(lid, pid)
    res = app.test_client().post("/decrease", data={"lid": -1, "pid": -1})
    assert res.json["message"] == product_not_found


def test_delete_from_stock():
    """Test deleting product from stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post("/delete-from-stock", data={"lid": lid, "pid": pid})
    assert res.status_code == 302
    assert get_product(lid, pid) is None
    res = app.test_client().post("/delete-from-stock", data={"lid": -1, "pid": -1})
    assert res.json["message"] == product_not_found

