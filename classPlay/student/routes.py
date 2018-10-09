from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from classPlay.student.forms import StudentRegistrationForm, UpdateStudentAccountForm
from classPlay import db, bcrypt
from classPlay.main.utils import user_redirect
from classPlay.student.models import Student
from classPlay.course.models import StudentCourse, Course
from classPlay.professor.models import Professor
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
    # filter(StudentCourse.student_id==current_user.id)
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
