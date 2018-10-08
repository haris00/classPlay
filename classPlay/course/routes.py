from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from classPlay.course.forms import CreateCourseForm
from classPlay.course.models import Course
from random import randint
from classPlay import db, bcrypt
from classPlay.main.utils import user_redirect

course = Blueprint('course', __name__)


@course.route("/professor/createCourse", methods=['GET', 'POST'])
@login_required
def professor_create_course():
    form = CreateCourseForm()
    if form.validate_on_submit():
        # This gives a random 6 digit number which we can use for join code.
        # Although unlikely, it is possible that it could produce a same random join code
        # that it already had produce
        join_code = randint(100000, 999999)
        course = Course(courseName=form.courseName.data, courseSection=form.courseSection.data,
                        joinCode=join_code, professorId=current_user.id)
        db.session.add(course)
        # TODO: Handle database unique constraint exception if same joinCode is given by the random function
        db.session.commit()
        return redirect(url_for('professor.account'))
    return render_template('professor/createCourse.html', professor=current_user, form=form)
