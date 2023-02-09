from app import app
from model.locations_service import LocationService


def get_lid() -> str:
    """Get the first location_id found."""
    lid = str(LocationService.get_all_locations()[0].id)
    return lid


def test_home() -> None:
    """Test routing to home."""
    assert app.test_client().get("/").status_code == 200


def test_location() -> None:
    """Test routing to '/locations'."""
    assert app.test_client().get("/locations").status_code == 200


def test_product() -> None:
    """Test routing to '/products'."""
    assert app.test_client().get("/products").status_code == 200


def test_edit_location() -> None:
    """Test routing to 'edit-location'."""
    assert app.test_client().get("/edit-location/" + get_lid()).status_code == 200


def test_stock() -> None:
    """Test routing to '/stock'."""
    assert app.test_client().get("/stock/" + get_lid()).status_code == 200
