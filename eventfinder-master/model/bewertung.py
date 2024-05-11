from repository.extension import db


class Bewertung(db.Model):
    __tablename__ = "bewertung"
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    kurzes_feedback = db.Column(db.String(255), nullable=True)
    langes_feedback = db.Column(db.Text, nullable=True)

    # Foreign key relationship to the Event model
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))

    def __init__(self, event, score, kurzes_feedback="", langes_feedback=""):
        self.event = event
        self.score = score
        self.kurzes_feedback = kurzes_feedback
        self.langes_feedback = langes_feedback

    def get_kurzes_feedback(self):
        return self.kurzes_feedback

    def get_langes_feedback(self):
        return self.langes_feedback

    def get_score(self):
        return self.score

    def get_event(self):
        return self.event

    def __repr__(self):
        return f"<Bewertung Score: {self.score}, Event ID: {self.event.id}>"
