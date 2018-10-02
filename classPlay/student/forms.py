from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from wtforms import SubmitField, PasswordField, StringField
from wtforms.validators import EqualTo, Length


class StudentRegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    firstName = StringField('First Name',
                            validators=[DataRequired(), Length(min=1, max=30)])
    lastName = StringField('Last Name',
                           validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    # TODO: Replace this with list of universities
    university = StringField('University',
                             validators=[DataRequired(), Length(min=1, max=30)])
    studentId = StringField('Student ID',
                             validators=[Length(min=1, max=30)])
    submit = SubmitField('Sign Up')