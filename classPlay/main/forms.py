from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email
from wtforms import BooleanField, SubmitField, PasswordField, StringField


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
