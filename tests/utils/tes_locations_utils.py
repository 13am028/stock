import secrets
import string
from typing import List

import model.locations_utils as utils
from model.model import Locations

success = "Success"
failure = "Database Failure"


def get_random_string(length: int) -> str:
    """Get a random string."""
    result_str = "".join(secrets.choice(string.ascii_letters) for _ in range(length))
    return result_str


def test_get_loc_name() -> None:
    """Test getting location name."""
    assert utils.get_loc_name("1") == "tests location"


def test_get_location() -> None:
    """Test getting location."""
    assert isinstance(utils.get_location("1"), Locations)
    assert utils.get_location("-1") is None


def test_get_all_locations() -> None:
    """Test getting all locations."""
    assert isinstance(utils.get_all_locations(), List)


def test_add_loc():
    """Test adding location."""
    location_name = get_random_string(7)
    assert utils.add_loc(location_name) == success
    assert utils.add_loc("tests location") == failure


def test_delete_loc():
    """Test deleting location."""
    location_id = utils.get_all_locations()[-1].id
    assert utils.delete_loc(location_id) == success
    assert utils.delete_loc(location_id) == "Location Not Found !"


def test_change_loc_name():
    """Test changing location name."""
    location_id = utils.get_all_locations()[-1].id
    assert utils.change_loc_name(location_id, get_random_string(5))
    assert utils.change_loc_name("-1", "blah") == "Location Not Found !"