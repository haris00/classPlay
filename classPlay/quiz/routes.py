from flask import Blueprint, request, abort
from flask_login import login_required, current_user
from classPlay.lib import get_quiz_state_in_redis
from classPlay.quiz.models import StudentQuizRunQuestionAttempt
from classPlay.sql_procedures.sql_procedures import insert_student_quiz_attempt_answer
import json


quiz = Blueprint('quiz', __name__)


@quiz.route("/quiz/api/get_quiz_state", methods=['GET'])
@login_required
def get_quiz_state():
    try:
        professor_id = request.args.get("professor_id")
        course_id = request.args.get("course_id")
    except KeyError:
        abort(400)
    quiz_state = get_quiz_state_in_redis(professor_id, course_id)
    return json.dumps(quiz_state), 200, {'ContentType': 'application/json'}


@quiz.route("/quiz/api/submit_answer", methods=['POST'])
@login_required
def submit_answer():
    data = request.json
    try:
        professor_id = data["professor_id"]
        course_id = data["course_id"]
        question_id = data["question_id"]
        quiz_id = data["quiz_id"]
        question_number = data["question_number"]
        answer_ids = data["answer_ids"]
    except KeyError:
        abort(400)
    quiz_state = get_quiz_state_in_redis(professor_id, course_id)
    return_data = dict()

    #TODO: Check if already answered

    if not quiz_state:
        return_data["message"] = "Quiz not running"
        return_data["submission_status"] = "error"
    elif int(quiz_state["question_number"]) != int(question_number):
        return_data["message"] = "Question not running"
        return_data["submission_status"] = "error"
    else:
        quiz_run_id = quiz_state["quiz_run_id"]
        student_quiz_answers_query = StudentQuizRunQuestionAttempt.query.\
            filter_by(quiz_run_id=quiz_run_id, student_id=current_user.id, question_id=question_id).first()
        if student_quiz_answers_query:
            return_data["message"] = "Question already answered"
            return_data["submission_status"] = "error"
        else:
            insert_student_quiz_attempt_answer(student_id=current_user.id, quiz_run_id=quiz_run_id, question_id=question_id,
                                               answer_ids=answer_ids)
            return_data["message"] = "Answered"
            return_data["submission_status"] = "success"

    return json.dumps(return_data), 200, {'ContentType': 'application/json'}

