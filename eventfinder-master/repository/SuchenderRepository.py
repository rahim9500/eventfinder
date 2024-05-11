from model.suchender import Suchender
from repository.extension import db


def add_suchender(suchender):
    """
    Add a new Suchender to the database.
    Args:
        suchender (Suchender): The Suchender object to be added to the database.
    """
    db.session.add(suchender)
    db.session.commit()


def set_suchender_telefon(suchender_id, new_telefon):
    suchender = Suchender.query.get(suchender_id)
    suchender.telefon = new_telefon
    db.session.commit()


def set_suchender_name(suchender_id, new_name):
    suchender = Suchender.query.get(suchender_id)
    suchender.name = new_name
    db.session.commit()


def set_suchender_mail(suchender_id, new_email):
    suchender = Suchender.query.get(suchender_id)
    suchender.mail = new_email
    db.session.commit()
