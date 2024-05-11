from repository.extension import db


class Teilnehmer(db.Model):
    __tablename__ = "teilnehmer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {"polymorphic_identity": "teilnehmer", "polymorphic_on": type}

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Teilnehmer {self.name}>"
