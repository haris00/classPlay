from flask import Blueprint, render_template
from classPlay.student.forms import StudentRegistrationForm
student = Blueprint('student', __name__)


@student.route("/studentRegister", methods=['GET', 'POST'])
def student_register():
    form = StudentRegistrationForm()
    return render_template('studentRegister.html', form=form)
