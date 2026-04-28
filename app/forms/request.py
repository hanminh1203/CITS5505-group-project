from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    SelectField,
    StringField,
    TextAreaField,
    validators,
)

from app.models import SessionFormat


class RequestForm(FlaskForm):
    id = HiddenField('id')
    version = HiddenField('version')
    title = StringField(
        'Request title',
        validators=[validators.DataRequired(), validators.Length(max=255)],
    )
    skill_to_learn = StringField('Skill you want to learn')
    skill_to_offer = SelectField(
        'Skills you are offering',
        coerce=int,
        validators=[validators.InputRequired()],
    )
    description = TextAreaField(
        'Description',
        validators=[validators.Length(max=1000)],
    )
    format = SelectField(
        'Session format',
        choices=[
            (session_format, session_format.value)
            for session_format in SessionFormat
        ],
    )
    duration = StringField('Duration per session')
    availability = StringField('Availability')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.skill_to_offer.choices = [
            (skill.id, skill.name) for skill in current_user.skills
        ]
