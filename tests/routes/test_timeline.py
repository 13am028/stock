import json

import path
from app import app

content_type_json = "application/json"
client = app.test_client()


class TestTimelineRoute:
    """Tests for /timeline routes."""

    def test_timeline_by_lid(self):
        """Test getting timeline by location id."""
        assert (
            client.post(
                path.GET_TIMELINE_BY_LOCATION,
                data=json.dumps({"location_id": 1}),
                content_type=content_type_json,
            ).status_code
            == 200
        )

    def test_timeline_by_pid(self):
        """Test getting timeline by product id."""
        assert (
            client.post(
                path.GET_TIMELINE_BY_PRODUCT,
                data=json.dumps({"product_id": 1}),
                content_type=content_type_json,
            ).status_code
            == 200
        )
