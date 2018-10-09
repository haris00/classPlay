from classPlay import db
from flask_login import UserMixin


class Quiz(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    quiz_number = db.Column(db.Integer, nullable=False)
    course_id = db.Column('course_id', db.Integer, db.ForeignKey("course.id"), nullable=False)
