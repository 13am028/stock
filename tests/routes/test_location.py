import json
import secrets
import string

import path
from app import app
from model.locations_service import LocationService

content_type_json = "application/json"
client = app.test_client()


def get_random_string(length: int) -> str:
    """Get a random string."""
    result_str = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return result_str


class TestLocationRoute:
    """Tests for /location routes."""

    def test_add_location(self) -> None:
        """Test adding a new location."""
        location_name = get_random_string(7)
        client.post(
            path.ADD_LOCATION_PATH,
            data=json.dumps({"location_name": location_name}),
            content_type=content_type_json,
        )
        assert location_name in [
            location.location_name for location in LocationService.get_all_locations()
        ]

    def test_change_location_name(self) -> None:
        """Test changing location name."""
        location_id: int = LocationService.add_location(get_random_string(5)).id
        rand_name: str = get_random_string(7)
        client.put(
            path.CHANGE_LOCATION_NAME_PATH,
            data=json.dumps({"location_id": location_id, "location_name": rand_name}),
            content_type=content_type_json,
        )
        for location in LocationService.get_all_locations():
            if location.id == location_id:
                assert location.location_name == rand_name

    def test_delete_location(self) -> None:
        """Test deleting location."""
        location_id: int = LocationService.add_location(get_random_string(5)).id
        client.delete(
            path.DELETE_LOCATION_PATH,
            data=json.dumps({"location_id": location_id}),
            content_type=content_type_json,
        )
        assert location_id not in [
            location.id for location in LocationService.get_all_locations()
        ]
