from flask import Blueprint
from classPlay.question.models import Question, QuizQuestion, MCQ, MCQAnswers


question = Blueprint('question', __name__)