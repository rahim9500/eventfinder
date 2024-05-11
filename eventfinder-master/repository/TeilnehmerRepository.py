from model.teilnehmer import Teilnehmer
from repository.extension import db


def get_teilnehmer_by_id(teilnehmer_id):
    return Teilnehmer.query.get(teilnehmer_id)


def add_teilnehmer(teilnehmer):
    """
    Add a new Teilnehmer to the database.
    Args:
        teilnehmer (Teilnehmer): The Teilnehmer object to be added to the database.
    """
    db.session.add(teilnehmer)
    db.session.commit()


def set_teilnehmer_name(teilnehmer_id, new_name):
    teilnehmer = Teilnehmer.query.get(teilnehmer_id)
    if teilnehmer:
        teilnehmer.name = new_name
        db.session.commit()
