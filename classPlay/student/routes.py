from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user, login_required
from classPlay.student.forms import StudentRegistrationForm
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


@student.route("/student/<string:username>", methods=['GET', 'POST'])
def student_account(username):
    return "Hallow {}".format(username)
