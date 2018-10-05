from classPlay import db
from flask_login import UserMixin


class Professor(db.Model, UserMixin):
    # We use same sequence for Id of both professor and student to uniquely identify them
    id = db.Column(db.Integer, db.Sequence('userId'), primary_key=True)
    userName = db.Column(db.String(20), unique=True, nullable=False)
    firstName = db.Column(db.String(20), unique=False, nullable=False)
    lastName = db.Column(db.String(20), unique=False, nullable=False)
    university = db.Column(db.String(40), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
