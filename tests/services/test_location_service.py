import secrets
import string
from typing import List

from app import app
from services.locations_service import LocationService
from model import Locations


def get_random_string(length: int) -> str:
    """Get a random string."""
    result_str = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return result_str


class TestLocationService:
    """Class containing methods for location."""

    with app.app_context():

        def test_get_location_name(self):
            """Get the location name given location id."""
            assert LocationService.get_location_name(1) == "test location"

        def test_get_location(self):
            """Get the location given location id."""
            assert isinstance(LocationService.get_location(1), Locations)

        def test_get_all_locations(self):
            """Get all locations."""
            assert isinstance(LocationService.get_all_locations(), List)

        def test_add_location(self):
            """Add new location."""
            location_name: str = get_random_string(5)
            assert isinstance(LocationService.add_location(location_name), Locations)

        def test_delete_location(self):
            """Delete location given location id."""
            location_name: str = get_random_string(5)
            to_delete = LocationService.add_location(location_name)
            assert LocationService.delete_location(to_delete.id) == to_delete

        def test_change_location_name(self):
            """Change location name."""
            location_name: str = get_random_string(5)
            new_name: str = get_random_string(5)
            to_change = LocationService.add_location(location_name)
            assert (
                LocationService.change_location_name(
                    to_change.id, new_name
                ).location_name
                == new_name
            )
