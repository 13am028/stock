import json
import secrets
import string

from app import app
from model.locations_utils import get_all_locations

location_uri = "/locations"
parser = "html.parser"
content_type_json = "application/json"


def get_random_string(length: int) -> str:
    """Get a random string."""
    result_str = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return result_str


def get_lid() -> str:
    """Get the first location_id found."""
    lid = str(get_all_locations()[0].id)
    return lid


def test_add_location() -> None:
    """Test adding a new location."""
    loc_name = get_random_string(7)
    app.test_client().post(
        "/add-location",
        data=json.dumps({"location": loc_name}),
        content_type=content_type_json,
    )
    assert loc_name in [loc.location_name for loc in get_all_locations()]


def test_change_loc_name() -> None:
    """Test changing location name."""
    lid = get_lid()
    rand_name = get_random_string(7)
    app.test_client().post(
        "/change-loc-name",
        data=json.dumps({"lid": lid, "location": rand_name}),
        content_type=content_type_json,
    )
    for location in get_all_locations():
        if str(location.id) == lid:
            assert location.location_name == rand_name


def test_delete_loc() -> None:
    """Test deleting location."""
    lid = get_lid()
    app.test_client().post(
        "/delete-loc", data=json.dumps({"lid": lid}), content_type=content_type_json
    )
    assert lid not in [location.id for location in get_all_locations()]
