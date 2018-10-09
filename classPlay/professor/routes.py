from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from classPlay import db, bcrypt
from classPlay.professor.forms import ProfessorRegistrationForm, UpdateProfessorAccountForm
from classPlay.main.utils import user_redirect
from classPlay.course.models import Course
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
    return render_template('professor/course_content.html', professor=current_user, course=course, active="content")


@professor.route("/professor/course/grades/<int:course_id>", methods=['GET', 'POST'])
@login_required
def course_grades(course_id):
    course = Course.query.filter_by(id=course_id).first()
    return render_template('professor/course_content.html', professor=current_user, course=course, active="grades")


@professor.route("/professor/course/students/<int:course_id>", methods=['GET', 'POST'])
@login_required
def course_students(course_id):
    course = Course.query.filter_by(id=course_id).first()
    return render_template('professor/course_content.html', professor=current_user, course=course, active="students")
