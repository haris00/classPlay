from classPlay import db
from flask_login import UserMixin


class Quiz(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    quizNumber = db.Column(db.Integer, nullable=False)
    courseId = db.Column('courseId', db.Integer, db.ForeignKey("course.id"), nullable=False)
