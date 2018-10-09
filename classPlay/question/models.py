from classPlay import db
from flask_login import UserMixin


class Question(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    question_type = db.Column(db.String(40), nullable=False)
    # in seconds
    time_limit = db.Column(db.Integer, nullable=False)


class QuizQuestion(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column('question_id', db.Integer, db.ForeignKey("question.id"), nullable=False)
    quiz_id = db.Column('quiz_id', db.Integer, db.ForeignKey("quiz.id"), nullable=False)


class MCQ(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # Making question Id unique ensures one-to-one mapping
    question_id = db.Column('question_id', db.Integer, db.ForeignKey("question.id"), unique=True, nullable=False)
    question_text = db.Column(db.String(), nullable=False)


class MCQAnswers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    option_text = db.Column(db.String(), nullable=False)
    correct_answer = db.Column(db.Boolean(), nullable=False, default=False)
    question_id = db.Column('MCQ_id', db.Integer, db.ForeignKey("MCQ.id"), nullable=False)
    option_number = db.Column(db.Integer, nullable=False)
