import datetime
from typing import List

from model.model import StockTimeline, db


class TimelineService:
    """Class containing methods for Timeline."""

    @classmethod
    def add_to_timeline(cls, lid: str, pid: str, stock: int) -> str:
        """Add product stock to timeline given location_id product_id."""
        new_stock_time: StockTimeline = StockTimeline(
            location_id=lid,
            product_id=pid,
            stock=stock,
            date=datetime.datetime.utcnow(),
        )
        with db.session() as session:
            session.add(new_stock_time)
            session.commit()

    @classmethod
    def get_timeline_by_location_id(cls, location_id: str) -> List[StockTimeline]:
        """Get timeline given vending machine location."""
        return StockTimeline.query.filter(
            StockTimeline.location_id == location_id
        ).all()

    @classmethod
    def get_timeline_by_product_id(cls, product_id: str) -> List[StockTimeline]:
        """Get timeline given product id."""
        return StockTimeline.query.filter(StockTimeline.product_id == product_id).all()
