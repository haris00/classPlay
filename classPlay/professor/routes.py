from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from classPlay import db, bcrypt
from classPlay.professor.forms import ProfessorRegistrationForm, UpdateProfessorAccountForm
from classPlay.main.utils import user_redirect
from classPlay.course.models import Course
from classPlay.professor.models import Professor

professor = Blueprint('professor', __name__)


@professor.route("/professorRegister", methods=['GET', 'POST'])
def professor_register():
    form = ProfessorRegistrationForm()
    if current_user.is_authenticated:
        return user_redirect(current_user)
    if form.validate_on_submit():
        form.validate_username(form.userName)
        form.validate_email(form.email)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        professor = Professor(userName=form.userName.data, firstName=form.firstName.data,
                              lastName=form.lastName.data, university=form.university.data, email=form.email.data,
                              password=hashed_password)
        db.session.add(professor)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('professorRegister.html', form=form)


@professor.route("/professor", methods=['GET', 'POST'])
@login_required
def professor_account():
    courses = Course.query.filter_by(professorId=current_user.id).all()
    return render_template('professorHome.html', professor=current_user, courses=courses)


@professor.route("/professor/account", methods=['GET', 'POST'])
@login_required
def professor_edit_account():
    form = UpdateProfessorAccountForm()
    if form.validate_on_submit():
        current_user.userName = form.userName.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('professor.professor_edit_account'))
    elif request.method == 'GET':
        form.userName.data = current_user.userName
        form.email.data = current_user.email
    return render_template('professorAccountUpdate.html', professor=current_user, form=form)
