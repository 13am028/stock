from bs4 import BeautifulSoup

from app import app

product_not_found = "Product Not Found !"


def get_lid() -> str:
    """Get the first location_id found."""
    html_page = app.test_client().get("/locations").data
    soup = BeautifulSoup(html_page, "html.parser")
    line = soup.find("li").find("a").get("href")
    lid = line[line.rfind("/") + 1 :]
    return lid


def get_pid() -> str:
    """Get the first product_id found."""
    html_page = app.test_client().get("/products").data
    soup = BeautifulSoup(html_page, "html.parser")
    pid = soup.find("input", {"name": "pid"}).get("value")
    return pid


def test_product_to_stock():
    """Test adding product to stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post(
        "/product-to-stock", data={"lid": lid, "pid": pid, "stock": 10}
    )
    assert res.status_code == 302
    res = app.test_client().post(
        "/product-to-stock", data={"lid": -1, "pid": -1, "stock": -1}
    )
    assert res.json["message"] == "Stock Cannot Be Negative !"


def test_increase_stock():
    """Test increasing stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post("/increase", data={"lid": lid, "pid": pid})
    assert res.status_code == 302
    res = app.test_client().post("/increase", data={"lid": -1, "pid": -1})
    assert res.json["message"] == product_not_found


def test_decrease_stock():
    """Test decreasing stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post("/decrease", data={"lid": lid, "pid": pid})
    assert res.status_code == 302
    res = app.test_client().post("/decrease", data={"lid": -1, "pid": -1})
    assert res.json["message"] == product_not_found


def test_delete_from_stock():
    """Test deleting product from stock."""
    lid = get_lid()
    pid = get_pid()
    res = app.test_client().post("/delete-from-stock", data={"lid": lid, "pid": pid})
    assert res.status_code == 302
    res = app.test_client().post("/delete-from-stock", data={"lid": -1, "pid": -1})
    assert res.json["message"] == product_not_found
