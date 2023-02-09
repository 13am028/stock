from typing import List

from model.model import Locations, Stock, StockTimeline, db


class LocationService:
    """Class containing methods for location."""

    @classmethod
    def get_location_name(cls, location_id: str) -> str:
        """Get the location name given location id."""
        return Locations.query.filter(Locations.id == location_id).first().location_name

    @classmethod
    def get_location(cls, location_id: str) -> Locations:
        """Get the location given location id."""
        return Locations.query.filter(Locations.id == location_id).first()

    @classmethod
    def get_all_locations(cls) -> List[Locations]:
        """Get all locations."""
        return Locations.query.all()

    @classmethod
    def add_location(cls, location_name: str) -> str:
        """Add new location."""
        new_location: Locations = Locations(location_name=location_name)
        with db.session() as session:
            session.add(new_location)
            session.commit()

    @classmethod
    def delete_location(cls, location_id: str) -> str:
        """Delete location given location id."""
        location: Locations = LocationService.get_location(location_id)
        if location is None:
            return "Location Not Found !"
        if location_id in [
            stock.product_id for stock in Stock.query.all()
        ] or location_id in [
            timeline.product_id for timeline in StockTimeline.query.all()
        ]:
            return "Location is still referenced"
        with db.session as session:
            session.delete(location)

    @classmethod
    def change_location_name(cls, lid: str, new_name: str) -> str:
        """Change location name."""
        location = Locations.query.filter(Locations.id == lid).first()
        if location is None:
            return "Location Not Found !"
        location.location_name = new_name
        with db.session as session:
            session.commit()
