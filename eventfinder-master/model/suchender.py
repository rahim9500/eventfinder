from repository.extension import db
from model.teilnehmer import Teilnehmer


class Suchender(Teilnehmer):
    __tablename__ = "suchender"
    id = db.Column(db.Integer, db.ForeignKey("teilnehmer.id"), primary_key=True)
    """
    should these attributes be nullable?
    => no, set as empty string instead
    """
    mail = db.Column(db.String(255), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "suchender",
    }

    def __init__(self, name, mail="", telefon=""):
        super().__init__(name)
        self.mail = mail
        self.telefon = telefon

    def __repr__(self):
        return f"<Suchender {self.name}>"
        return f"<Suchender {self.name}>"

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "mail": self.mail,
            "telefon": self.telefon,
        }

    @staticmethod
    def deserialize(suchender_data):
        suchender = Suchender(
            name=suchender_data["name"],
            mail=suchender_data["mail"],
            telefon=suchender_data["telefon"],
        )
        if "id" in suchender_data:
            suchender.id = suchender_data["id"]
        return suchender
