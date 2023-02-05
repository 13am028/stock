from app import app
from model.locations_utils import get_all_locations
from model.model import Stock
from model.products_utils import get_all_products
from model.stock_utils import decrease_stock, delete_stock, increase_stock, product_to_stock

with app.app_context():
    pass


def test_product_to_stock():
    """Test adding product to location stock."""
    assert product_to_stock("-1", "-1", -1) == "Stock Cannot Be Negative !"
    location = get_all_locations()[-1].id
    product = get_all_products()[-1].id
    assert product_to_stock(location, product, 0) == "Success"


def test_increase_stock():
    """Test increasing product stock."""
    assert increase_stock("-1", "-1") == "Product Not Found !"


def test_decrease_stock():
    """Test decreasing product stock."""
    assert decrease_stock("-1", "-1") == "Product Not Found !"
    stock = Stock.query.first()
    assert decrease_stock(stock.location_id, stock.product_id) == "Success"


def test_delete_stock():
    """Test deleting product from location."""
    assert delete_stock("-1", "-1") == "Product Not Found !"
