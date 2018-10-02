from flask import Blueprint, render_template
from classPlay.professor.forms import ProfessorRegistrationForm
professor = Blueprint('professor', __name__)


@professor.route("/professorRegister", methods=['GET', 'POST'])
def professor_register():
    form = ProfessorRegistrationForm()
    return render_template('professorRegister.html', form=form)
