# Imports
from datetime import date
from model.event import Event
from model.kategorie import Kategorie
from model.suchender import Suchender
from model.teilnehmer import Teilnehmer
from model.bewertung import Bewertung
from model.alter import Alter
from model.status import Status
from repository import BewertungRepository, EventRepository
from repository.KategorieRepository import add_kategorie, delete_kategorie_by_id
from repository.extension import db
from app import app

# Tests for the EventRepository
with app.app_context():
    db.create_all()

    kategorie1 = Kategorie(name="Music")
    kategorie2 = Kategorie(name="Art")

    add_kategorie(kategorie1)
    add_kategorie(kategorie2)

    suchender1 = Suchender(name="John Doe", mail="john@example.com")
    suchender2 = Suchender(name="Jane Doe", mail="jane@example.com")
    teilnehmer1 = Teilnehmer(name="Alice")
    teilnehmer2 = Teilnehmer(name="Bob")

    db.session.add(suchender1)
    db.session.add(suchender2)
    db.session.add(teilnehmer1)
    db.session.add(teilnehmer2)
    db.session.commit()

    event = Event(
        name="Sample Event",
        dauer=2,
        ort="Sample Location",
        datum=date.today(),
        uhrzeit="18:00",
        altersgruppe=Alter.UEBER_18,
        preis=20.0,
        status=Status.AKTIV,
        gesuchte_teilnehmer_anzahl=50,
        suchender=suchender1,
        kategorien=[kategorie1, kategorie2],
        teilnehmer=[teilnehmer1, teilnehmer2],
    )
    EventRepository.add_event(event)

    print()

    # Test getting an event by ID
    retrieved_event = EventRepository.get_event_by_id(event.id)
    print("Retrieved Event by ID:", retrieved_event)

    # Test getting an event by name
    retrieved_events_by_name = EventRepository.get_event_by_name("Sample Event")
    print("Retrieved Event by Name: ", retrieved_events_by_name)

    # Test getting all events
    all_events = EventRepository.get_all_events()
    print("All Events:")
    for event in all_events:
        print(event)

    # Test setting an event attribute
    EventRepository.set_event_attribute(event.id, "name", "Updated Event Name")
    updated_event = EventRepository.get_event_by_id(event.id)
    print("Updated Event Name:", updated_event.name)

    # Test getting event attributes
    event_name = EventRepository.get_event_attribute(event.id, "name")
    event_ort = EventRepository.get_event_attribute(event.id, "ort")
    print(f"Event Name: {event_name}, Event Ort: {event_ort}")

    # Add a new teilnehmer and delete an existing one
    new_teilnehmer = Teilnehmer(name="Charlie")
    db.session.add(new_teilnehmer)
    db.session.commit()
    EventRepository.add_event_teilnehmer(event.id, new_teilnehmer)
    EventRepository.delete_event_teilnehmer_by_name(event.id, "Alice")
    updated_teilnehmer_list = EventRepository.get_event_teilnehmer_liste(event.id)
    print("Updated Event Teilnehmer List:")
    for t in updated_teilnehmer_list:
        print(t.name)

    # Test adding and getting event Bewertungen
    bewertung1 = Bewertung(event, "Great event", 4)
    bewertung2 = Bewertung(event, "Bad event", 1)
    BewertungRepository.add_event_bewertung(bewertung1)
    BewertungRepository.add_event_bewertung(bewertung2)

    BewertungRepository.set_bewertung_event_by_id(bewertung1.id, event.id)
    BewertungRepository.set_bewertung_event_by_id(bewertung2.id, event.id)

    event_bewertungen = EventRepository.get_event_bewertungen(event.id)
    print("Event Bewertungen:")
    for b in event_bewertungen:
        print(f"Rating: {b.score}, Text: {b.kurzes_feedback}")

    # Test deleting a Kategorie used in an event
    try:
        delete_kategorie_by_id(kategorie1.id)
    except Exception as e:
        print("Failed to delete Kategorie:", e)
