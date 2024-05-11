from model.bewertung import Bewertung
from model.event import Event
from model.suchender import Suchender
from repository import TeilnehmerRepository
from repository.extension import db


def get_event_by_id(event_id):
    return Event.query.get(event_id)


def get_event_by_id_with_session(event_id):
    with db.session() as session:
        return session.query(Event).get(event_id)


def get_event_by_name(name):
    return Event.query.filter_by(name=name).all()


def get_all_events():
    return Event.query.all()


def add_event(event):
    db.session.add(event)
    db.session.commit()
    return event


def delete_event_by_id(event_id):
    event_to_delete = get_event_by_id(event_id)
    if event_to_delete:
        db.session.delete(event_to_delete)
        db.session.commit()


def add_event_kategorie(event_id, kategorie):
    event = get_event_by_id(event_id)
    if event:
        # Check if Kategorie is already in the session
        if not db.session.identity_key(instance=kategorie) in db.session.identity_map:
            db.session.add(kategorie)
            db.session.commit()  # Commit here to ensure Kategorie is persisted before associating

        # Now add Kategorie to the event
        event.kategorien.append(kategorie)
        db.session.commit()


def get_event_kategorien(event_id):
    event = get_event_by_id(event_id)
    if event:
        return event.kategorien
    return []


def get_aktuelle_teilnehmer_anzahl(event_id):
    event = get_event_by_id(event_id)
    if event:
        return event.aktuelle_teilnehmer_anzahl()

    else:
        return -1


def get_suchender_name_for_event(event_id):
    event = get_event_by_id(event_id)
    if event and event.suchender:
        return event.suchender.name
    return None


def get_event_attribute(event_id, attribute):
    """
    event_name = get_event_attribute(event_id, 'name')

    :param event_id
    :param attribute: name of attribute in class event
    :return: None if no event found
    """
    event = get_event_by_id(event_id)
    if event:
        return getattr(event, attribute, None)
    return None


# Methods to set attributes of an event
def set_event_attribute(event_id, attribute, value):
    event = get_event_by_id(event_id)
    if event:
        setattr(event, attribute, value)
        db.session.commit()


def get_event_teilnehmer_by_name(event_id, teilnehmer_name):
    """ """
    event = get_event_by_id(event_id)
    if event:
        return [t for t in event.teilnehmer if t.name == teilnehmer_name]
    return None


def get_event_teilnehmer_by_id(event_id, teilnehmer_id):
    """
    Retrieve a specific Teilnehmer by their ID for a given event.

    Args:
        event_id (int): The ID of the event.
        teilnehmer_id (int): The ID of the Teilnehmer.

    Returns:
        Teilnehmer: teilnehmer, raises ValueError if not found
    """
    event = get_event_by_id(event_id)
    if event:
        for teilnehmer in event.teilnehmer:
            if teilnehmer.id == teilnehmer_id:
                return teilnehmer
        raise ValueError(
            f"Found no teilnehmer with ID {teilnehmer_id} for event with ID{event_id}"
        )
    raise ValueError(f"No event found with ID {event_id}")


def add_event_teilnehmer(event_id, teilnehmer):
    """
    Add a Teilnehmer to an event. Persist Teilnehmer if not already persisted.
    Args:
        event_id (int): The ID of the event.
        teilnehmer (Teilnehmer): The Teilnehmer object to be added to the event.
    """
    event = get_event_by_id(event_id)
    if event:
        # Check if Teilnehmer is already in the session
        if not db.session.identity_key(instance=teilnehmer) in db.session.identity_map:
            db.session.add(teilnehmer)
        event.teilnehmer.append(teilnehmer)
        db.session.commit()


def get_event_teilnehmer_liste(event_id):
    """
    Returns a list of Teilnehmer for a given event. Raises an exception if the event is not found.
    Args:
        event_id (int): The ID of the event.
    Returns:
        list[Teilnehmer]: List of Teilnehmer associated with the event.
    """
    event = get_event_by_id(event_id)
    if event:
        return event.teilnehmer
    else:
        raise ValueError(f"No event found with ID {event_id}")


def delete_event_teilnehmer_by_name(event_id, teilnehmer_name):
    """
    Args:
        event_id (int): The ID of the event.
        teilnehmer_name (str): The name of the Teilnehmer to be removed from the event.
    """
    event = get_event_by_id(event_id)
    if event:
        # Find the Teilnehmer with the matching name
        teilnehmer_to_remove = None
        for teilnehmer in event.teilnehmer:
            if teilnehmer.name == teilnehmer_name:
                teilnehmer_to_remove = teilnehmer
                break

        # Remove the Teilnehmer from the event if found
        if teilnehmer_to_remove:
            event.teilnehmer.remove(teilnehmer_to_remove)
            db.session.commit()


def delete_event_teilnehmer_by_id(event_id, teilnehmer_id):
    event = get_event_by_id(event_id)
    teilnehmer = TeilnehmerRepository.get_teilnehmer_by_id(teilnehmer_id)

    if event and teilnehmer:
        if teilnehmer in event.teilnehmer:
            event.teilnehmer.remove(teilnehmer)
            db.session.commit()
    else:
        raise ValueError(
            f"No event with ID {event_id} or teilnehmer with ID {teilnehmer_id} found."
        )


def get_event_bewertungen(event_id):
    return Bewertung.query.filter_by(event_id=event_id).all()


@staticmethod
def get_event_by_token(token):
    # Sucht das Event anhand des Bestätigungstokens
    return Event.query.filter_by(confirmation_token=token).first()


@staticmethod
def get_event_by_email_and_token(email, token):
    return (
        Event.query.join(Suchender)
        .filter(Event.confirmation_token == token, Suchender.email == email)
        .first()
    )
