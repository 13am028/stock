import model.stock_utils as utils
from model.locations_utils import get_all_locations
from model.model import Stock
from model.products_utils import get_all_products

product_not_found = "Product Not Found !"


def test_product_to_stock():
    """Test adding product to location stock."""
    assert utils.product_to_stock("-1", "-1", -1) == "Stock Cannot Be Negative !"
    location = get_all_locations()[-1].id
    product = get_all_products()[-1].id
    assert utils.product_to_stock(location, product, 0) == "Success"


def test_increase_stock():
    """Test increasing product stock."""
    assert utils.increase_stock("-1", "-1") == product_not_found


def test_decrease_stock():
    """Test decreasing product stock."""
    assert utils.decrease_stock("-1", "-1") == product_not_found
    stock = Stock.query.first()
    assert utils.decrease_stock(stock.location_id, stock.product_id) == "Success"


def test_delete_stock():
    """Test deleting product from location."""
    assert utils.delete_stock("-1", "-1") == product_not_found
