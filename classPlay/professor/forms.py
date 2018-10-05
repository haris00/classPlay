from classPlay.main.forms import RegistrationForm
from wtforms.validators import ValidationError
from classPlay.professor.models import Professor
from classPlay.student.models import Student


class ProfessorRegistrationForm(RegistrationForm):
    def validate_username(self, username):
        professor_user = Professor.query.filter_by(userName=username.data).first()
        if professor_user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        professor_user = Professor.query.filter_by(email=email.data).first()
        student_user = Student.query.filter_by(email=email.data).first()
        if professor_user or student_user:
            raise ValidationError('That email is taken. Please choose a different one.')

