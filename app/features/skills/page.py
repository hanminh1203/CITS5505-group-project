from flask import Blueprint, render_template, request
from app.extensions import db
from app.forms.skill import SkillForm
from app.models import Skill

skills_views_bp = Blueprint("skills_views", __name__)


@skills_views_bp.route("/modals/skill", methods=['GET'])
def display_skill_modal():
    skill_id = request.args.get('skill_id')
    if skill_id:
        entity = db.get_or_404(Skill, skill_id)
        form = SkillForm(obj=entity)
        is_new = False
    else:
        form = SkillForm()
        is_new = True
    return render_template(
        "modals/skill.modal.html", form=form, is_new=is_new
    )
