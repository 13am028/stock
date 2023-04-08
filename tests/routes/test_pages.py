import path
from app import app
from services.locations_service import LocationService


def get_lid() -> str:
    """Get the first location_id found."""
    lid = str(LocationService.get_all_locations()[0].id)
    return lid


client = app.test_client()


class TestPages:
    """Tests for pages that return render_template."""

    def test_home(self) -> None:
        """Test routing to home."""
        assert client.get("/").status_code == 200

    def test_location(self) -> None:
        """Test routing to '/locations'."""
        assert client.get(path.ALL_LOCATIONS_PATH).status_code == 200

    def test_product(self) -> None:
        """Test routing to '/products'."""
        assert client.get(path.ALL_PRODUCTS_PATH).status_code == 200

    def test_edit_location(self) -> None:
        """Test routing to 'edit-location'."""
        assert client.get("/location/edit-location/" + get_lid()).status_code == 200

    def test_stock(self) -> None:
        """Test routing to '/stock'."""
        assert client.get("/stock/detail/" + get_lid()).status_code == 200

    def test_stock_timeline(self) -> None:
        """Test routing to '/stock'."""
        assert client.get(path.STOCK_TIMELINE_PATH).status_code == 200
