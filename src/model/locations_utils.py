from typing import List

from model.model import Locations, session, session_commit


def get_loc_name(lid: str) -> str:
    """Get the location name given location id."""
    return Locations.query.filter(Locations.id == lid).first().location_name


def get_location(lid: str) -> Locations:
    """Get the location given location id."""
    return Locations.query.filter(Locations.id == lid).first()


def get_all_locations() -> List[Locations]:
    """Get all locations."""
    return Locations.query.all()


def add_loc(location_name: str) -> str:
    """Add new location."""
    new_location: Locations = Locations(location_name=location_name)
    session.add(new_location)
    return session_commit()


def delete_loc(lid: str) -> str:
    """Delete location given location id."""
    loc: Locations = get_location(lid)
    if loc is None:
        return "Location Not Found !"
    session.delete(loc)
    return session_commit()


def change_loc_name(lid: str, new_name: str) -> str:
    """Change location name."""
    location = Locations.query.filter(Locations.id == lid).first()
    if location is None:
        return "Location Not Found !"
    location.location_name = new_name
    return session_commit()
