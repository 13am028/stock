import secrets
import string

from bs4 import BeautifulSoup

from app import app

product_uri = "/products"
parser = "html.parser"


def get_random_string(length: int) -> str:
    """Get a random string."""
    result_str = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return result_str


def get_pid() -> str:
    """Get the first product_id found."""
    html_page = app.test_client().get(product_uri).data
    soup = BeautifulSoup(html_page, parser)
    pid = soup.find("input", {"name": "pid"}).get("value")
    return pid


def test_add_product() -> None:
    """Test adding a new product."""
    product_name = get_random_string(7)
    app.test_client().post("/add-product", data={"product": product_name})

    html_page = app.test_client().get(product_uri).data
    soup = BeautifulSoup(html_page, parser)
    products = []
    for name in soup.findAll("h3"):
        products.append(name.getText())
    assert product_name in products


def test_delete_product() -> None:
    """Test deleting product."""
    pid = get_pid()
    app.test_client().post("/delete-product", data={"pid": pid})
    html_page = app.test_client().get(product_uri).data
    soup = BeautifulSoup(html_page, parser)
    assert soup.find("h3", {"id": pid}) is None
