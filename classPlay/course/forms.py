from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
from wtforms import BooleanField, SubmitField, PasswordField, StringField
from flask_login import current_user


class CreateCourseForm(FlaskForm):
    courseName = StringField('Course Name',
                             validators=[DataRequired(), Length(min=2, max=80)])
    courseSection = StringField('Course Section',
                                validators=[DataRequired(), Length(min=1, max=40)])
    submit = SubmitField('Create')
