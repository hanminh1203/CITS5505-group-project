from flask import Blueprint, jsonify

from models import User

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.order_by(User.id).all()
    return jsonify([{"id": u.id, "name": u.email} for u in users])
