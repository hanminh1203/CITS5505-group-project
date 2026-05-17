from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


# Form class for validating user profile updates
class ProfileForm(FlaskForm):
    name = StringField(
        "Display name",
        validators=[
            # It is a function from WTForms, it makes this field mandatory
            DataRequired(),
            Length(min=3, max=255, message="Name is at least 3 characters"),
        ],
    )
    # Bio and address are optional
    bio = TextAreaField("Bio")
    address = StringField("Location", validators=[Length(max=255)])
