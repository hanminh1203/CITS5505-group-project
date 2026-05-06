from flask import Blueprint, jsonify, request
from flask_login import current_user

from app.exceptions import ValidationException
from app.extensions import db
from app.forms import ProfileForm
from app.models import User

users_api_bp = Blueprint("users", __name__, url_prefix="/users")


@users_api_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.order_by(User.id).all()
    return jsonify([{"id": user.id, "name": user.email} for user in users])


@users_api_bp.route("/me", methods=["PUT"])
def update_profile():
    if not current_user.is_authenticated:
        return jsonify(error="Unauthorized"), 401

    dto = ProfileForm(obj=request.form)
    if not dto.validate():
        raise ValidationException(dto.errors)

    user = db.session.get(User, current_user.id)
    user.name = dto.name.data
    user.bio = dto.bio.data
    user.address = dto.address.data

    db.session.commit()
    return jsonify(id=user.id), 200
