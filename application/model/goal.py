from application import db


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
