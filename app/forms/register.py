from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(),
            Length(
                min=3,
                message="Name must be at least 3 characters.",
            ),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email address."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=8,
                message="Password must be at least 8 characters.",
            ),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Confirm password must match password.",
            ),
        ],
    )
    