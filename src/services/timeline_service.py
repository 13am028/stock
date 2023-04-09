from typing import List

from model import StockTimeline, session


class TimelineService:
    """Class containing methods for Timeline."""

    @classmethod
    def add_to_timeline(
        cls, location_id: int, product_id: int, stock: int
    ) -> StockTimeline:
        """Add product stock to timeline given location_id product_id."""
        new_stock_time: StockTimeline = StockTimeline(
            location_id=location_id,
            product_id=product_id,
            stock=stock,
        )
        session.add(new_stock_time)
        session.commit()
        return new_stock_time

    @classmethod
    def get_timeline_by_location_id(cls, location_id: int) -> List[StockTimeline]:
        """Get timeline given vending machine location."""
        return StockTimeline.query.filter(
            StockTimeline.location_id == location_id
        ).all()

    @classmethod
    def get_timeline_by_product_id(cls, product_id: int) -> List[StockTimeline]:
        """Get timeline given product id."""
        return StockTimeline.query.filter(StockTimeline.product_id == product_id).all()

    @classmethod
    def all_timelines_to_dict(cls, timelines: List[StockTimeline]) -> List:
        """Convert all timelines to List of Dict."""
        return [stock.to_dict() for stock in timelines]
