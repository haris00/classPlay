from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from classPlay.student.forms import StudentRegistrationForm, UpdateStudentAccountForm
from classPlay import db, bcrypt
from classPlay.main.utils import user_redirect
from classPlay.student.models import Student
from classPlay.course.models import StudentCourse, Course
from classPlay.professor.models import Professor
from classPlay.quiz.models import Quiz
from classPlay.metrics.lib import student_scores
from classPlay.lib import get_quiz_content, get_quiz_state_in_redis
from classPlay import db

student = Blueprint('student', __name__)


@student.route("/studentRegister", methods=['GET', 'POST'])
def register():
    form = StudentRegistrationForm()
    if current_user.is_authenticated:
        return user_redirect(current_user)
    if form.validate_on_submit():
        form.validate_user_name(form.user_name)
        form.validate_email(form.email)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(user_name=form.user_name.data, first_name=form.first_name.data,
                          student_id=form.student_id.data, last_name=form.last_name.data,
                          university=form.university.data, email=form.email.data,
                          password=hashed_password)
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('student/register.html', form=form)


@student.route("/student", methods=['GET', 'POST'])
@login_required
def account():
    student_courses = db.session.query(StudentCourse, Course, Professor).join(Course, Professor).filter(StudentCourse.student_id==current_user.id).all()
    return render_template('student/home.html', student=current_user, student_courses=student_courses)


@student.route("/student/account", methods=['GET', 'POST'])
@login_required
def edit_account():
    form = UpdateStudentAccountForm()
    if form.validate_on_submit():
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('student.edit_account'))
    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
    return render_template('student/account_update.html', student=current_user, form=form)


@student.route("/student/course/quiz/<int:course_id>", methods=['GET', 'POST'])
@login_required
def course_quiz(course_id):
    course = Course.query.filter_by(id=course_id).first()
    professor = db.session.query(Professor.id).join(Course).filter(Course.id == course_id).first()
    professor_id = professor[0]
    current_quiz_state = get_quiz_state_in_redis(professor_id=professor_id, course_id=course_id)
    if current_quiz_state:
        if current_quiz_state.get("time_limit", "not_set") != "not_set":
            quiz_id = current_quiz_state["quiz_id"]
            quizes = Quiz.query.filter_by(id=quiz_id, course_id=course_id).all()
            quiz_content_object = get_quiz_content(quizes, quiz_id=quiz_id)[0]
            question_number = int(current_quiz_state["question_number"])
            mcq_options = quiz_content_object["questions"][question_number - 1]["mcq_options"]
            quiz_number = quiz_content_object["quiz_number"]
            question_text = quiz_content_object["questions"][question_number - 1]["question_text"]
            question_id = quiz_content_object["questions"][question_number - 1]["question_id"]
            return render_template('student/running_quiz.html', student=current_user, course=course,
                                   mcq_options=mcq_options, professor=professor, question_id=question_id,
                                   question_text=question_text, question_number=question_number, quiz_id=quiz_id,
                                   quiz_number=quiz_number, active="content")
    return render_template('student/course_quiz.html', student=current_user, course=course, active="quiz")


@student.route("/student/course/scoreBook/<int:course_id>", methods=['GET', 'POST'])
@login_required
def course_score_book(course_id):
    course = Course.query.filter_by(id=course_id).first()
    scores = student_scores(student_id=current_user.id, course_id=course_id)
    return render_template('student/score_book.html', student=current_user, course=course,
                           scores=scores, active="score_book")
