from typing import List

from app import app
from services.timeline_service import TimelineService


class TestTimelineService:
    """Class containing methods for Timeline."""

    with app.app_context():

        def test_get_timeline_by_location_id(self):
            """Get timeline given vending machine location."""
            assert isinstance(TimelineService.get_timeline_by_location_id(1), List)

        def test_get_timeline_by_product_id(self):
            """Get timeline given product id."""
            assert isinstance(TimelineService.get_timeline_by_product_id(1), List)

        def test_all_timelines_to_dict(self):
            """Convert all timelines to List of Dict."""
            timelines = TimelineService.get_timeline_by_product_id(1)
            assert isinstance(TimelineService.all_timelines_to_dict(timelines), List)
