from bs4 import BeautifulSoup

from app import app

product_not_found = "Product Not Found !"
stock_uri = "/stock/"
parser = "html.parser"


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
    """Get current stock of a product."""
    html_page = app.test_client().get(stock_uri + lid).data
    soup = BeautifulSoup(html_page, parser)
    stock = soup.find("div", {"id": pid}).find("h4").getText().split()[-1]
    return int(stock)


def test_product_to_stock():
    """Test adding product to stock."""
    uri = "/product-to-stock"
    lid = get_lid()
    pid = get_pid()
    res_success = app.test_client().post(uri, data={"lid": lid, "pid": pid, "stock": 0})
    assert res_success.status_code == 302


def test_increase_stock():
    """Test increasing stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post("/increase", data={"lid": lid, "pid": pid})
    assert res.status_code == 302


def test_decrease_stock():
    """Test decreasing stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post("/decrease", data={"lid": lid, "pid": pid})
    assert res.status_code == 302


def test_delete_from_stock():
    """Test deleting product from stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post("/delete-from-stock", data={"lid": lid, "pid": pid})
    assert res.status_code == 302
