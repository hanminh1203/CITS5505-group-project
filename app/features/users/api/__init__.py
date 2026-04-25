from flask import Blueprint, jsonify

from app.models import User

users_api_bp = Blueprint("users", __name__, url_prefix="/users")


@users_api_bp.route("/", methods=["GET"])
def get_users():
    users = User.query.order_by(User.id).all()
    return jsonify([{"id": user.id, "name": user.email} for user in users])


__all__ = ["users_api_bp"]