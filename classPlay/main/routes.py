from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from classPlay import bcrypt
from classPlay.main.forms import LoginForm
from classPlay.main.utils import user_redirect
from classPlay.student.models import Student
from classPlay.professor.models import Professor
main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/login", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return user_redirect(current_user)
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        professor = Professor.query.filter_by(email=form.email.data).first()
        incorrect_credentials_msg = "Login Unsuccessful. Incorrect username or password"
        if student:
            if bcrypt.check_password_hash(student.password, form.password.data):
                login_user(student, remember=form.remember.data)
                return redirect(url_for('student.student_account', id=student.id))
            else:
                flash(incorrect_credentials_msg, 'danger')
        elif professor:
            if bcrypt.check_password_hash(professor.password, form.password.data):
                login_user(professor, remember=form.remember.data)
                return redirect(url_for('professor.professor_account', id=professor.id))
            else:
                flash(incorrect_credentials_msg, 'danger')
        elif not (student or professor):
            flash('Login Unsuccessful. The account does not exists', 'danger')

    return render_template('login.html', form=form)


@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template('register.html')


@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.login'))