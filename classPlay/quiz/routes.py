from flask import Blueprint, request, abort
from flask_login import login_required
from classPlay.quiz.models import Quiz
from classPlay.lib import get_quiz_state_in_redis
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
