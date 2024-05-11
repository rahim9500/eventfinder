from model.event import Event
from model.kategorie import Kategorie
from repository.extension import db


def add_kategorie(kategorie):
    """Add a new Kategorie to the database."""
    db.session.add(kategorie)
    db.session.commit()


def get_kategorie_by_name(name):
    """Retrieve a Kategorie by its name."""
    return Kategorie.query.filter_by(name=name).first()


def set_kategorie_name_by_id(kategorie_id, new_name):
    """Set the name of a Kategorie by its ID"""
    kategorie = Kategorie.query.get(kategorie_id)
    if kategorie:
        kategorie.name = new_name
        db.session.commit()


def set_kategorie_name(kategorie, new_name):
    """
    Set the name of a Kategorie by the kategorie itself instead of ID

    Args:
        kategorie (Kategorie): The Kategorie object whose name is to be updated.
        new_name (str): The new name for the Kategorie.
    """
    if kategorie:
        kategorie.name = new_name
        db.session.commit()


def get_kategorie_by_id(kategorie_id):
    """Retrieve a Kategorie by its ID."""
    return Kategorie.query.get(kategorie_id)


def get_all_kategorien():
    """Retrieve all Kategorien."""
    return Kategorie.query.all()


def delete_kategorie_by_id(kategorie_id):
    """Delete a Kategorie by its ID (Primary key) and its associations in events."""
    kategorie = Kategorie.query.get(kategorie_id)
    if kategorie:
        # Remove association from events
        events = Event.query.filter(Event.kategorien.any(id=kategorie_id)).all()
        for event in events:
            event.kategorien.remove(kategorie)

        # Now delete the kategorie
        db.session.delete(kategorie)
        db.session.commit()


def get_kategorie_attribute(kategorie_id, attribute):
    kategorie = Kategorie.query.get(kategorie_id)
    if kategorie:
        return getattr(kategorie, attribute, None)
    return None


def set_kategorie_attribute(kategorie_id, attribute, value):
    kategorie = Kategorie.query.get(kategorie_id)
    if kategorie:
        setattr(kategorie, attribute, value)
        db.session.commit()


def get_kategorie_name_by_object(kategorie):
    return Kategorie.query.get(kategorie).name
