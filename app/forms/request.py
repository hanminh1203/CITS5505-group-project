from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    SelectField,
    StringField,
    TextAreaField,
    validators,
)
from wtforms_sqlalchemy.fields import QuerySelectField

from app.models import SessionFormat


def coerce_none(value):
    if value is None or value == 'None' or value == '':
        return None
    return str(value)


class RequestForm(FlaskForm):
    id = HiddenField('id')
    version = HiddenField('version')
    title = StringField(
        'Request title',
        validators=[
            validators.DataRequired(),
            validators.Length(max=255)
        ],
    )
    skill_to_learn = StringField(
        'Skill you want to learn',
        validators=[
            validators.DataRequired(),
            validators.Length(max=255)
        ],
    )
    owner_skill = QuerySelectField(
        label='Skill you are offering',
        query_factory=lambda: current_user.skills,
        get_label='name',
        allow_blank=True,
        blank_text='',
        validators=[validators.InputRequired()]
    )
    description = TextAreaField(
        'Description',
        validators=[validators.Length(max=1000)],
    )
    format = SelectField(
        'Session format',
        choices=[(None, '')] + [
            (session_format, session_format.value)
            for session_format in SessionFormat
        ],
        coerce=coerce_none
    )
    duration = StringField(
        'Duration per session',
        validators=[validators.Length(max=255)]
    )
    availability = StringField(
        'Availability',
        validators=[validators.Length(max=255)]
    )
