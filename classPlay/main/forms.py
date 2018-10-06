from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, ValidationError, Length, EqualTo
from wtforms import BooleanField, SubmitField, PasswordField, StringField
from flask_login import current_user


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):

    userName = StringField('Username',
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
    submit = SubmitField('Sign Up')


class UpdateAccountForm(FlaskForm):
    userName = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')