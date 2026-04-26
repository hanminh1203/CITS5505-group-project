from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField


class LoginForm(FlaskForm):
    email = EmailField('Email')
    password = PasswordField('Password')
    