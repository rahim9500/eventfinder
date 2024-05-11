from model.bewertung import Bewertung
from model.event import Event
from repository.extension import db


def get_bewertung_attribute(bewertung_id, attribute):
    bewertung = Bewertung.query.get(bewertung_id)
    if bewertung:
        return getattr(bewertung, attribute, None)
    return None


def set_bewertung_attribute(bewertung_id, attribute, value):
    bewertung = Bewertung.query.get(bewertung_id)
    if bewertung:
        setattr(bewertung, attribute, value)
        db.session.commit()


def add_event_bewertung(bewertung):
    """
    Add a new Bewertung to the database.

    Args:
        bewertung (Bewertung): The Bewertung object to be added to the database.
    """
    db.session.add(bewertung)
    db.session.commit()


def set_bewertung_score(bewertung_id, new_score):
    bewertung = Bewertung.query.get(bewertung_id)
    bewertung.score = new_score
    db.session.commit()


def update_bewertung_kurzes_feedback(bewertung_id, new_kurzes_feedback):
    bewertung = Bewertung.query.get(bewertung_id)
    bewertung.kurzes_feedback = new_kurzes_feedback
    db.session.commit()


def update_bewertung_langes_feedback(bewertung_id, new_langes_feedback):
    bewertung = Bewertung.query.get(bewertung_id)
    bewertung.langes_feedback = new_langes_feedback
    db.session.commit()


def set_bewertung_event_by_id(bewertung_id, new_event_id):
    """
    Update the event associated with a specific Bewertung.

    Args:
        bewertung_id (int): The ID of the Bewertung to update.
        new_event_id (int): The ID of the new Event to associate with the Bewertung.
    """
    bewertung = Bewertung.query.get(bewertung_id)
    new_event = Event.query.get(new_event_id)

    if bewertung and new_event:
        bewertung.event_id = new_event.id
        db.session.commit()
    elif not bewertung:
        raise ValueError(f"Bewertung with ID {bewertung_id} not found.")
    elif not new_event:
        raise ValueError(f"Event with ID {new_event_id} not found.")
