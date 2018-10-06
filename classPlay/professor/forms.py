from classPlay.main.forms import RegistrationForm, UpdateAccountForm
from wtforms.validators import ValidationError
from classPlay.professor.models import Professor
from classPlay.student.models import Student
from flask_login import current_user


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


class UpdateProfessorAccountForm(UpdateAccountForm):

    def validate_username(self, username):
        if username.data != current_user.userName:
            professor = Professor.query.filter_by(username=userName.data).first()
            if professor:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            # Professor and Student cannot use the same email.
            # Otherwise, it won't be able to identify student from professor
            professor_user = Professor.query.filter_by(email=email.data).first()
            student_user = Student.query.filter_by(email=email.data).first()
            if professor_user or student_user:
                raise ValidationError('That email is taken. Please choose a different one.')