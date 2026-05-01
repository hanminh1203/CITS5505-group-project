from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.exceptions import NotAuthorizedActionException, ValidationException
from app.extensions import db
from app.forms import SkillForm
from app.models import Skill
from app.models.enums import SkillLevel

skills_api_bp = Blueprint("skills", __name__, url_prefix="/skills")


# Add a new skill
@skills_api_bp.route("/", methods=["POST"])
def add_skill():
    # Validate incoming form data
    dto = SkillForm(obj=request.form)
    if not dto.validate():
        raise ValidationException(dto.errors)

    # Create new skill bound to the current user
    entity = Skill()
    entity.user_id = current_user.id
    entity.name = dto.name.data
    entity.level = SkillLevel(dto.level.data)
    entity.description = dto.description.data

    db.session.add(entity)
    db.session.commit()
    return jsonify(id=entity.id), 200


# Update an existing skill
@skills_api_bp.route("/<int:skill_id>", methods=["POST"])
def update_skill(skill_id):
    # Validate incoming form data
    dto = SkillForm(obj=request.form)
    if not dto.validate():
        raise ValidationException(dto.errors)

    entity = db.get_or_404(Skill, skill_id)
    
    # Ensure user owns this skill
    if entity.user_id != current_user.id:
        raise NotAuthorizedActionException()

    # Update fields
    entity.name = dto.name.data
    entity.level = SkillLevel(dto.level.data)
    entity.description = dto.description.data

    db.session.commit()
    return jsonify(id=entity.id), 200


# Delete a specific skill
@skills_api_bp.route("/<int:skill_id>/delete", methods=["POST"])
def delete_skill(skill_id):
    entity = db.get_or_404(Skill, skill_id)
    
    # Ensure user owns this skill before deletion
    if entity.user_id != current_user.id:
        raise NotAuthorizedActionException()

    db.session.delete(entity)
    db.session.commit()
    return "", 200
