from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import current_user, login_required
from classPlay import db, bcrypt
from classPlay.professor.forms import ProfessorRegistrationForm, UpdateProfessorAccountForm
from classPlay.main.utils import user_redirect
from classPlay.course.models import Course, StudentCourse
from classPlay.student.models import Student
from classPlay.quiz.models import Quiz, QuizRun
from classPlay.question.models import Question
from classPlay.lib import get_quiz_content, set_quiz_state_in_redis, get_quiz_state_in_redis, \
    delete_quiz_state_in_redis
from classPlay.professor.models import Professor
import json
from classPlay.sql_procedures.sql_procedures import create_quiz_run
from classPlay.metrics.lib import student_scores, answers_selected, get_correct_answers
from classPlay.professor.lib import get_chart_from_answers

professor = Blueprint('professor', __name__)


@professor.route("/professor_register", methods=['GET', 'POST'])
def register():
    form = ProfessorRegistrationForm()
    if current_user.is_authenticated:
        return user_redirect(current_user)
    if form.validate_on_submit():
        form.validate_username(form.user_name)
        form.validate_email(form.email)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        professor = Professor(user_name=form.user_name.data, first_name=form.first_name.data,
                              last_name=form.last_name.data, university=form.university.data, email=form.email.data,
                              password=hashed_password)
        db.session.add(professor)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('professor/register.html', form=form)


@professor.route("/professor", methods=['GET', 'POST'])
@login_required
def account():
    courses = Course.query.filter_by(professor_id=current_user.id).all()
    return render_template('professor/home.html', professor=current_user, courses=courses)


@professor.route("/professor/account", methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateProfessorAccountForm()
    if form.validate_on_submit():
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('professor.edit_account'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
    return render_template('professor/account_update.html', professor=current_user, form=form)


@professor.route("/professor/course/content/<int:course_id>", methods=['GET', 'POST'])
@login_required
def course_content(course_id):
    course = Course.query.filter_by(id=course_id).first()
    quiz_running_state = get_quiz_state_in_redis(professor_id=current_user.id, course_id=course_id)
    if quiz_running_state:
        return redirect(url_for('professor.get_running_quiz',
                                course_id=course_id, quiz_id = quiz_running_state["quiz_id"]))
    quizes = Quiz.query.filter_by(course_id=course_id).all()
    quiz_content_object = get_quiz_content(quizes)

    return render_template('professor/course_content.html', professor=current_user, course=course,
                           quiz_content_object=quiz_content_object , active="content")


@professor.route("/professor/course/score_book/<int:course_id>", methods=['GET', 'POST'])
@login_required
def score_book(course_id):
    course = Course.query.filter_by(id=course_id).first()
    students = db.session.query(Student).join(StudentCourse).filter(
        Course.id == course_id).all()
    return render_template('professor/score_book.html', professor=current_user, course=course,
                           students=students, active="score_book")


@professor.route("/professor/course/student_score_book/<int:course_id>/<int:student_id>", methods=['GET', 'POST'])
@login_required
def student_score_book(course_id, student_id):
    student = Student.query.filter_by(id=student_id).first()
    course = Course.query.filter_by(id=course_id).first()
    scores = student_scores(student_id=student_id, course_id=course_id)
    return render_template('professor/student_score_book.html', student=student, course=course,
                           scores=scores, active="score_book")


@professor.route("/professor/course/question_metrics/<int:course_id>/<int:quiz_run_id>/<int:question_id>", methods=['GET'])
@login_required
def question_metrics(course_id, quiz_run_id, question_id):
    course, question, chart, quiz, quiz_run = _question_metric(course_id, quiz_run_id, question_id)
    return render_template('professor/question_metrics.html', professor=current_user, course=course, question=question,
                           chart=chart, quiz=quiz, quiz_run=quiz_run, active="score_book")


def question_metrics_with_timer(course_id, quiz_run_id, question_id, professor_id, question_number):
    course, question, chart, quiz, quiz_run = _question_metric(course_id, quiz_run_id, question_id)
    return render_template('professor/question_metrics_with_timer.html', professor=current_user, course=course,
                           question=question, chart=chart, quiz=quiz, quiz_run=quiz_run, professor_id=professor_id,
                           question_number=question_number, active="score_book")


def _question_metric(course_id, quiz_run_id, question_id):
    answers = answers_selected(quiz_run_id, question_id)
    correct_answers = get_correct_answers(question_id)
    chart = get_chart_from_answers(answers, correct_answers)
    course = Course.query.filter_by(id=course_id).first()
    question = Question.query.filter_by(id=question_id).first()
    quiz_run = QuizRun.query.filter_by(id=quiz_run_id).first()
    quiz = Quiz.query.filter_by(id=quiz_run.quiz_id).first()

    return course, question, chart, quiz, quiz_run


@professor.route("/professor/course/content/start_quiz/<int:course_id>/<int:quiz_id>", methods=['GET', 'POST'])
@login_required
def start_quiz(course_id, quiz_id):
    # TODO: Throw error specifically why quiz not started
    # The app should never allow to start quiz if it's already running
    if get_quiz_state_in_redis(professor_id=current_user, course_id=course_id) is None:
        abort(400)
    quiz_run_id = create_quiz_run(quiz_id)
    current_quiz_state = {
        "status": "running",
        "question_number": 1,
        "time_limit": "not_set",
        "quiz_id": quiz_id,
        "quiz_run_id": quiz_run_id
    }
    set_quiz_state_in_redis(professor_id=current_user.id, course_id=course_id, state=current_quiz_state)
    return redirect(url_for('professor.get_running_quiz', course_id=course_id, quiz_id=quiz_id))


@professor.route("/professor/course/content/end_quiz/<int:course_id>", methods=['GET', 'POST'])
@login_required
def end_quiz(course_id):
    delete_quiz_state_in_redis(professor_id=current_user.id, course_id=course_id)
    # TODO: Return to histogram page showing statistics
    return redirect(url_for('professor.course_content', course_id=course_id))


@professor.route("/professor/course/content/get_running_quiz/<int:course_id>/<int:quiz_id>/", methods=['GET', 'POST'])
@login_required
def get_running_quiz(course_id, quiz_id):
    course = Course.query.filter_by(id=course_id).first()
    quizes = Quiz.query.filter_by(id=quiz_id, course_id=course_id).all()
    quiz_content_object = get_quiz_content(quizes)[0]
    # Stop the quiz if there is no questions (or don't let it run)
    total_questions = len(quiz_content_object["questions"])
    current_quiz_state = get_quiz_state_in_redis(professor_id=current_user.id, course_id=course_id)
    if not current_quiz_state:
        return redirect(url_for('professor.course_content', course_id=course_id))

    question_number = int(current_quiz_state["question_number"])

    if "metrics" in current_quiz_state["status"]:
        return question_metrics_with_timer(course_id=course_id,
                                           quiz_run_id=current_quiz_state["quiz_run_id"],
                                           question_id=quiz_content_object["questions"][question_number-1]["question_id"],
                                           professor_id=current_user.id, question_number=question_number)

    if total_questions == 0 or question_number > total_questions or question_number < 0:
        return redirect(url_for('professor.end_quiz', course_id=course_id))
    mcq_options = quiz_content_object["questions"][question_number-1]["mcq_options"]
    quiz_number = quiz_content_object["quiz_number"]
    question_text = quiz_content_object["questions"][question_number-1]["question_text"]
    if current_quiz_state.get("time_limit", "not_set") == "not_set":
        time_limit = quiz_content_object["questions"][question_number-1]["time_limit"]
        set_quiz_state_in_redis(professor_id=current_user.id, course_id=course_id, state={"time_limit": time_limit})
    else:
        time_limit = current_quiz_state.get("time_limit")
    return render_template('professor/run_quiz.html', professor=current_user, course=course, mcq_options=mcq_options,
                           question_text=question_text, time_limit=time_limit, total_questions=total_questions,
                           question_number=question_number, quiz_number=quiz_number, active="content")


# Only professor can set the quiz state. Therefore we keep this route in professor blueprint
@professor.route("/professor/api/set_quiz_state", methods=['POST'])
@login_required
def set_quiz_state():
    """
    Sets the state of a running quiz
    Takes json data in post request in the form
    {
    "professor_id":1,
    "course_id":1,
    "state":
        {
            "quiz_id":<quiz_id>,
            "status":"paused",
            ...
        }
    }
    And sets the quiz state in redis with following schema:
    "running_quizes":<professor_id>:<course_id>:
    {
        {
            "status": "paused",
            ...
        }
    }

    :return:
    """
    if not request.json:
        abort(400)
    try:
        data = request.json
        professor_id = data["professor_id"]
        course_id = data["course_id"]
        state = data["state"]
    except KeyError:
        abort(400)
    set_quiz_state_in_redis(professor_id, course_id, state)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}