from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    validators,
)
from wtforms_sqlalchemy.fields import QuerySelectField


class OfferForm(FlaskForm):
    skill = QuerySelectField(
        label='Skill you are offering',
        query_factory=lambda: current_user.skills,
        get_label=lambda skill: skill.get_label(),
        allow_blank=True,
        blank_text='<Select a skill from your profile>',
        validators=[validators.DataRequired()]
    )
    message = TextAreaField(
        'Message to request owner',
        validators=[validators.Length(max=1000)],
    )
