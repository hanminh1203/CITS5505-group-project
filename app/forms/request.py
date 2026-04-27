from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectField, StringField, TextAreaField

from app.models import SessionFormat


class RequestForm(FlaskForm):
    id = HiddenField('id')
    version = HiddenField('version')
    title = StringField('Request title')
    skill_to_learn = StringField('Skill you want to learn')
    skill_to_offer = StringField('Skills you are offering')
    description = TextAreaField('Description')
    format = SelectField('Session format',
                         choices=[(session_format, session_format.value) for session_format in SessionFormat])
    duration = StringField('Duration per session')
    availability = StringField('Availability')
