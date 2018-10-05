from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from classPlay import db, bcrypt
from classPlay.professor.forms import ProfessorRegistrationForm
from classPlay.main.utils import user_redirect
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


@professor.route("/professor/<int:id>", methods=['GET', 'POST'])
@login_required
def professor_account(id):
    professor = Professor.query.filter_by(id=id).first()
    return render_template('professorHome.html', professor=professor)
