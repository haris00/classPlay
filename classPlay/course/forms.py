from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo, NumberRange
from wtforms import BooleanField, SubmitField, PasswordField, StringField, IntegerField
from flask_login import current_user


class CreateCourseForm(FlaskForm):
    course_name = StringField('Course Name',
                             validators=[DataRequired(), Length(min=2, max=80)])
    course_section = StringField('Course Section',
                                validators=[DataRequired(), Length(min=1, max=40)])
    submit = SubmitField('Create')


class JoinCourseForm(FlaskForm):
    join_code = IntegerField('Join Code',
                            validators=[DataRequired()])
    submit = SubmitField('Join')

    def validate_join_code(form, field):
        exact_len = 6
        if len(str(field.data)) != exact_len:
            raise ValidationError('Join Code must be equal to {}'.format(exact_len))