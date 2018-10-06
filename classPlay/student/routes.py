from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from classPlay.student.forms import StudentRegistrationForm, UpdateStudentAccountForm
from classPlay import db, bcrypt
from classPlay.main.utils import user_redirect
from classPlay.student.models import Student

student = Blueprint('student', __name__)


@student.route("/studentRegister", methods=['GET', 'POST'])
def student_register():
    form = StudentRegistrationForm()
    if current_user.is_authenticated:
        return user_redirect(current_user)
    if form.validate_on_submit():
        form.validate_username(form.userName)
        form.validate_email(form.email)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(userName=form.userName.data, firstName=form.firstName.data,
                          studentId=form.studentId.data, lastName=form.lastName.data,
                          university=form.university.data, email=form.email.data,
                          password=hashed_password)
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('studentRegister.html', form=form)


@student.route("/student", methods=['GET', 'POST'])
@login_required
def student_account():
    return render_template('studentHome.html', student=current_user)


@student.route("/student/account", methods=['GET', 'POST'])
@login_required
def student_edit_account():
    form = UpdateStudentAccountForm()
    if form.validate_on_submit():
        current_user.userName = form.userName.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('student.student_edit_account'))
    elif request.method == 'GET':
        form.userName.data = current_user.userName
        form.email.data = current_user.email
    return render_template('studentAccountUpdate.html', student=current_user, form=form)
