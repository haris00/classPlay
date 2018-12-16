from classPlay import db
from flask_login import UserMixin
from datetime import datetime


class Quiz(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    quiz_number = db.Column(db.Integer, nullable=False)
    course_id = db.Column('course_id', db.Integer, db.ForeignKey("course.id"), nullable=False)


class QuizRun(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    run_number = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column('quiz_id', db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    quiz_run_start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class StudentQuizRunQuestionAttempt(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column('student_id', db.Integer, db.ForeignKey("student.id"), nullable=False)
    quiz_run_id = db.Column('quiz_run_id', db.Integer, db.ForeignKey("quiz_run.id"), nullable=False)
    question_id = db.Column('question_id', db.Integer, db.ForeignKey("question.id"), nullable=False)


class StudentQuizRunAnswers(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    student_quiz_run_question_attempt_id = db.Column('student_quiz_run_question_attempt_id',
                                                     db.Integer, db.ForeignKey("student_quiz_run_question_attempt.id"),
                                                     nullable=False)
    # This answer id is not a foreign key to answer table because we don't know the exact type (MCQ, Fill in the blank
    # etc) of question
    answer_id = db.Column(db.Integer)
