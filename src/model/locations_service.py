from typing import List

from model.model import Locations, session


class LocationService:
    """Class containing methods for location."""

    @classmethod
    def get_location_name(cls, location_id: int) -> str:
        """Get the location name given location id."""
        return Locations.query.filter(Locations.id == location_id).first().location_name

    @classmethod
    def get_location(cls, location_id: int) -> Locations:
        """Get the location given location id."""
        return Locations.query.filter(Locations.id == location_id).first()

    @classmethod
    def get_all_locations(cls) -> List[Locations]:
        """Get all locations."""
        return Locations.query.all()

    @classmethod
    def add_location(cls, location_name: str) -> Locations:
        """Add new location."""
        new_location: Locations = Locations(location_name=location_name)
        session.add(new_location)
        session.commit()
        return new_location

    @classmethod
    def delete_location(cls, location_id: int) -> Locations:
        """Delete location given location id."""
        location: Locations = LocationService.get_location(location_id)
        session.delete(location)
        session.commit()
        return location

    @classmethod
    def change_location_name(cls, location_id: int, new_name: str) -> Locations:
        """Change location name."""
        location = Locations.query.filter(Locations.id == location_id).first()
        location.location_name = new_name
        session.commit()
        return location
