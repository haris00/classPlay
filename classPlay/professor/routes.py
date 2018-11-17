from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from classPlay import db, bcrypt
from classPlay.professor.forms import ProfessorRegistrationForm, UpdateProfessorAccountForm
from classPlay.main.utils import user_redirect
from classPlay.course.models import Course
from classPlay.quiz.models import Quiz
from classPlay.question.models import QuizQuestion, Question, MCQ, MCQAnswers
from classPlay.professor.models import Professor

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
    quizes = Quiz.query.filter_by(course_id=course_id).all()
    course_content_object = []
    for quiz in quizes:
        quiz_content = dict()
        quiz_content["quiz_id"] = quiz.id
        quiz_content["quiz_number"] = quiz.quiz_number
        course_content_object.append(quiz_content)

    for quiz_index, quiz in enumerate(course_content_object):
        quiz_questions = QuizQuestion.query.filter_by(quiz_id=quiz["quiz_id"]).all()
        course_content_object[quiz_index]["questions"] = []
        for question_index, question in enumerate(quiz_questions):
            question = Question.query.filter_by(id=question.id).first()
            question_content = dict()
            question_content["time_limit"] = question.time_limit
            question_content["question_id"] = question.id
            question_content["question_number"] = question.question_number
            if question.question_type == "MCQ":
                mcq_question = MCQ.query.filter_by(question_id=question.id).first()
                question_content["question_text"] = mcq_question.question_text
                mcq_answers = MCQAnswers.query.filter_by(question_id=mcq_question.id).all()
                mcq_options = []
                for mcq_answer in mcq_answers:
                    mcq_options_content = dict()
                    mcq_options_content["option_text"] = mcq_answer.option_text
                    mcq_options_content["correct_answer"] = mcq_answer.correct_answer
                    mcq_options.append(mcq_options_content)
                question_content["mcq_options"] = mcq_options
                course_content_object[quiz_index]["questions"].append(question_content)
            else:
                continue

    return render_template('professor/course_content.html', professor=current_user, course=course,
                           course_content_object=course_content_object, active="content")


@professor.route("/professor/course/grades/<int:course_id>", methods=['GET', 'POST'])
@login_required
def course_grades(course_id):
    course = Course.query.filter_by(id=course_id).first()
    return render_template('professor/course_grades.html', professor=current_user, course=course, active="grades")


@professor.route("/professor/course/students/<int:course_id>", methods=['GET', 'POST'])
@login_required
def course_students(course_id):
    course = Course.query.filter_by(id=course_id).first()
    return render_template('professor/course_students.html', professor=current_user, course=course, active="students")
