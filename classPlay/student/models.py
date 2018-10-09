from classPlay import db
from flask_login import UserMixin


class Student(db.Model, UserMixin):
    # We use same sequence for Id of both professor and student to uniquely identify them
    id = db.Column(db.Integer, db.Sequence('user_id'), primary_key=True)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    university = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    student_id = db.Column(db.String(60), nullable=True)
