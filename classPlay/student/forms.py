from wtforms import StringField
from wtforms.validators import Length
from classPlay.main.forms import RegistrationForm
from wtforms.validators import ValidationError
from classPlay.student.models import Student
from classPlay.professor.models import Professor


class StudentRegistrationForm(RegistrationForm):
    studentId = StringField('Student ID', validators=[Length(min=1, max=30)])

    def validate_username(self, username):
        student_user = Student.query.filter_by(userName=username.data).first()
        if student_user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        # Professor and Student cannot use the same email.
        # Otherwise, we won't be able to identify student from professor
        student_user = Student.query.filter_by(email=email.data).first()
        professor_user = Professor.query.filter_by(email=email.data).first()
        if professor_user or student_user:
            raise ValidationError('That email is taken. Please choose a different one.')