from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from classPlay.course.forms import CreateCourseForm, JoinCourseForm
from classPlay.course.models import Course, StudentCourse
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
        course = Course(course_name=form.course_name.data, course_section=form.course_section.data,
                        join_code=join_code, professor_id=current_user.id)
        db.session.add(course)
        # TODO: Handle database unique constraint exception if same join_code is given by the random function
        db.session.commit()
        return redirect(url_for('professor.account'))
    return render_template('professor/create_course.html', professor=current_user, form=form)


@course.route("/student/join_course", methods=['GET', 'POST'])
@login_required
def student_join_course():
    form = JoinCourseForm()
    if form.validate_on_submit():
        course = Course.query.filter_by(join_code=form.join_code.data).first()
        if not course:
            flash('Course by this join code does not exist', 'danger')
        else:
            # TODO: Use Enums (with only two possibility registered/dropped) for status
            student_course = StudentCourse(student_id=current_user.id, course_id=course.id, status="registered")
            db.session.add(student_course)
            db.session.commit()
            return redirect(url_for('student.account'))
    return render_template('student/join_course.html', student=current_user, form=form)
