from repository.extension import db
from model.kategorie import Kategorie
from model.suchender import Suchender
from datetime import datetime
from model.alter import Alter
from model.status import Status
from sqlalchemy import Enum


class Event(db.Model):
    __tablename__ = "event"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    dauer = db.Column(db.Integer, nullable=False)
    ort = db.Column(db.String, nullable=False)
    datum = db.Column(db.Date, nullable=False)
    uhrzeit = db.Column(db.String, nullable=False)
    altersgruppe = db.Column(Enum(Alter), nullable=False)
    preis = db.Column(db.Float, nullable=False)
    status = db.Column(Enum(Status), nullable=False)
    gesuchte_teilnehmer_anzahl = db.Column(db.Integer, nullable=False)
    confirmation_token = db.Column(db.String(255), unique=True, nullable=True)

    # Relationships
    # One-to-one relationship with Suchender
    suchender_id = db.Column(db.Integer, db.ForeignKey("suchender.id"))
    suchender = db.relationship("Suchender", backref=db.backref("event", uselist=False))
    # One-to-many relationship with Kategorie
    kategorien = db.relationship(
        "Kategorie", secondary="event_kategorie", backref="events"
    )
    # One-to-many relationship with Teilnehmer
    teilnehmer = db.relationship(
        "Teilnehmer", secondary="event_teilnehmer", backref="events"
    )

    @property
    def aktuelle_teilnehmer_anzahl(self):
        """instead of having a field to the anzahl, the len of list is returned"""
        return len(self.teilnehmer)

    def __init__(
        self,
        name,
        dauer,
        ort,
        datum,
        uhrzeit,
        altersgruppe,
        preis,
        status,
        gesuchte_teilnehmer_anzahl,
        suchender,
        kategorien,
        teilnehmer=None,
    ):
        self.name = name
        self.dauer = dauer
        self.ort = ort
        self.datum = datum
        self.uhrzeit = uhrzeit
        self.altersgruppe = altersgruppe
        self.preis = preis
        self.status = status
        self.gesuchte_teilnehmer_anzahl = gesuchte_teilnehmer_anzahl
        self.suchender = suchender
        self.kategorien = kategorien
        self.teilnehmer = teilnehmer if teilnehmer is not None else []

    def __repr__(self):
        return f"<Event {self.name}>"

    # Association tables for many-to-many relationships

    def serialize(self):
        """Konvertiert das Event-Objekt in ein Dictionary zur Speicherung in einer Session."""
        return {
            "id": self.id,
            "name": self.name,
            "dauer": self.dauer,
            "ort": self.ort,
            "datum": self.datum.isoformat(),
            "uhrzeit": self.uhrzeit,
            "altersgruppe": self.altersgruppe,
            "preis": self.preis,
            "status": self.status,
            "gesuchte_teilnehmer_anzahl": self.gesuchte_teilnehmer_anzahl,
            "suchender_id": self.suchender_id,
            "kategorien": [kategorie.id for kategorie in self.kategorien],
        }

    @staticmethod
    def deserialize(event_data):
        """Erstellt ein Event-Objekt aus einem Dictionary."""
        event = Event(
            name=event_data["name"],
            dauer=event_data["dauer"],
            ort=event_data["ort"],
            datum=datetime.strptime(event_data["datum"], "%Y-%m-%d").date(),
            uhrzeit=event_data["uhrzeit"],
            altersgruppe=event_data["altersgruppe"],
            preis=event_data["preis"],
            status=event_data["status"],
            gesuchte_teilnehmer_anzahl=event_data["gesuchte_teilnehmer_anzahl"],
            suchender=Suchender.query.get(event_data["suchender_id"]),
            kategorien=[Kategorie.query.get(k_id) for k_id in event_data["kategorien"]],
        )
        return event


event_kategorie = db.Table(
    "event_kategorie",
    db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
    db.Column(
        "kategorie_id", db.Integer, db.ForeignKey("kategorie.id"), primary_key=True
    ),
)

event_teilnehmer = db.Table(
    "event_teilnehmer",
    db.Column("event_id", db.Integer, db.ForeignKey("event.id"), primary_key=True),
    db.Column(
        "teilnehmer_id", db.Integer, db.ForeignKey("teilnehmer.id"), primary_key=True
    ),
)
