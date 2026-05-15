from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.exceptions import ValidationException
from app.extensions import db
from app.forms import ProfileForm
from app.models import User

users_api_bp = Blueprint("users", __name__, url_prefix="/users")


@users_api_bp.route("/me", methods=["PUT"])
def update_profile():
    dto = ProfileForm(obj=request.form)
    if not dto.validate():
        raise ValidationException(dto.errors)

    user = db.get_or_404(User, current_user.id)
    user.name = dto.name.data
    user.bio = dto.bio.data
    user.address = dto.address.data

    db.session.commit()
    return jsonify(id=user.id), 200
