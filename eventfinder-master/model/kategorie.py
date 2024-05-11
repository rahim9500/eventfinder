from repository.extension import db


class Kategorie(db.Model):
    __tablename__ = "kategorie"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Kategorie {self.name}>"
