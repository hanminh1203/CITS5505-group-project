from flask_wtf import FlaskForm
from wtforms import (
    HiddenField,
    SelectField,
    StringField,
    TextAreaField,
    validators,
)

from app.models.enums import SkillLevel


class SkillForm(FlaskForm):
    id = HiddenField('id')
    version = HiddenField('version')
    name = StringField(
        'Skill name',
        validators=[
            validators.DataRequired(),
            validators.Length(min=2, max=255)
        ]
    )
    level = SelectField(
        'Proficiency level',
        choices=[(lvl.value, lvl.value) for lvl in SkillLevel],
        validators=[validators.DataRequired()]
    )
    description = TextAreaField(
        'Brief description',
        validators=[validators.Length(max=1000)]
    )
