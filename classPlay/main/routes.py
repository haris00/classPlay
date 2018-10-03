from flask import Blueprint, render_template, redirect, url_for, flash
from classPlay import bcrypt
from classPlay.main.forms import LoginForm
from classPlay.student.models import Student
from classPlay.professor.models import Professor
main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        professor = Professor.query.filter_by(email=form.email.data).first()
        incorrect_credentials_msg = "Login Unsuccessful. Incorrect username or password"
        if student:
            if bcrypt.check_password_hash(student.password, form.password.data):
                return render_template('replace.html', form=form)
            else:
                flash(incorrect_credentials_msg, 'danger')
        elif professor:
            if bcrypt.check_password_hash(professor.password, form.password.data):
                return render_template('replace.html', form=form)
            else:
                flash(incorrect_credentials_msg, 'danger')
        elif not (student or professor):
            flash('Login Unsuccessful. The account does not exists', 'danger')

    return render_template('login.html', form=form)


@main.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')
