from classPlay import db
from flask_login import UserMixin


class Course(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(80), nullable=False)
    courseSection = db.Column(db.String(40), nullable=True)
    professorId = db.Column('professorId', db.Integer, db.ForeignKey("professor.id"), nullable=False)
    joinCode = db.Column('joinCode', db.Integer, unique=True, nullable=False)
