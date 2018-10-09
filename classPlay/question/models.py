from classPlay import db
from flask_login import UserMixin


class Question(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    questionType = db.Column(db.String(40), nullable=False)
    # in seconds
    timeLimit = db.Column(db.Integer, nullable=False)


class QuizQuestion(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    questionID = db.Column('questionId', db.Integer, db.ForeignKey("question.id"), nullable=False)
    quizID = db.Column('quizId', db.Integer, db.ForeignKey("quiz.id"), nullable=False)


class MCQ(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # Making question Id unique ensures one-to-one mapping
    questionID = db.Column('questionId', db.Integer, db.ForeignKey("question.id"), unique=True, nullable=False)
    questionText = db.Column(db.String(), nullable=False)


class MCQAnswers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    optionText = db.Column(db.String(), nullable=False)
    correctAnswer = db.Column(db.Boolean(), nullable=False, default=False)
    questionID = db.Column('MCQId', db.Integer, db.ForeignKey("MCQ.id"), nullable=False)
    optionNumber = db.Column(db.Integer, nullable=False)
