from wtforms import StringField
from wtforms.validators import Length
from classPlay.main.forms import RegistrationForm, UpdateAccountForm
from wtforms.validators import ValidationError
from classPlay.student.models import Student
from classPlay.professor.models import Professor
from flask_login import current_user


class StudentRegistrationForm(RegistrationForm):
    student_id = StringField('Student ID', validators=[Length(min=1, max=30)])

    def validate_user_name(self, user_name):
        student_user = Student.query.filter_by(user_name=user_name.data).first()
        if student_user:
            raise ValidationError('That user_name is taken. Please choose a different one.')

    def validate_email(self, email):
        # Professor and Student cannot use the same email.
        # Otherwise, it won't be able to identify student from professor
        student_user = Student.query.filter_by(email=email.data).first()
        professor_user = Professor.query.filter_by(email=email.data).first()
        if professor_user or student_user:
            raise ValidationError('That email is taken. Please choose a different one.')


class UpdateStudentAccountForm(UpdateAccountForm):

    def validate_user_name(self, user_name):
        if user_name.data != current_user.user_name:
            student = Student.query.filter_by(user_name=user_name.data).first()
            if student:
                raise ValidationError('That user_name is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            # Professor and Student cannot use the same email.
            # Otherwise, it won't be able to identify student from professor
            professor_user = Professor.query.filter_by(email=email.data).first()
            student_user = Student.query.filter_by(email=email.data).first()
            if professor_user or student_user:
                raise ValidationError('That email is taken. Please choose a different one.')