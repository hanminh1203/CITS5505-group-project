from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class ProfileForm(FlaskForm):
    name = StringField(
        "Display name", validators=[DataRequired(), Length(min=3, max=255, message="Name is at least 3 characters")]
    )
    bio = TextAreaField("Bio")
    address = StringField("Location", validators=[Length(max=255)])
