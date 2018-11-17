"""This routes (and sql_procedure module) is temporary measure so that we can insert data from get request
this is JUST FOR CONVENIENCE. The only file to be used eventually is 'sql_procedures.py"""
from flask import Blueprint
from sql_procedures import create_quiz, create_question, create_mcq_option
sql_procedures = Blueprint('sql_procedures', __name__)


@sql_procedures.route("/sql_procedure/create_quiz/<int:course_id>", methods=['GET', 'POST'])
def sql_create_quiz(course_id):
    create_quiz(course_id)


@sql_procedures.route("/sql_procedure/create_question/<int:course_id>/"
                      "<int:quiz_number>/<int:time_limit>/<string:question_text>", methods=['GET', 'POST'])
def sql_create_question(course_id, quiz_number, time_limit, question_text):
    create_question(course_id, quiz_number, time_limit, question_text)


@sql_procedures.route("/sql_procedure/create_question_option/<int:course_id>/"
                      "<int:quiz_number>/<int:question_number>/<string:option_text>/"
                      "<int:correct_answer>", methods=['GET', 'POST'])
def sql_create_question_option(course_id, quiz_number, question_number, option_text, correct_answer):
    if correct_answer == 0:
        correct_answer = False
    else:
        correct_answer = True
    create_mcq_option(course_id, quiz_number, question_number, option_text, correct_answer)
