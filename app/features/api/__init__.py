from flask import Blueprint, request
from flask_login import login_required, login_user

from app.exceptions import InvalidCredientialException, ValidationException
from app.features.requests.api import requests_api_bp
from app.features.skills.api import skills_api_bp
from app.features.users.api import users_api_bp
from app.forms import LoginForm
from app.models import User

public_api_bp = Blueprint("public_api", __name__, url_prefix="/api")


@public_api_bp.route("/login", methods=['POST'])
def authenticate():
    dto = LoginForm(obj=request.form)
    if not dto.validate():
        raise ValidationException(dto.errors)
    user = User.query.filter_by(email=dto.email.data).first()
    if not user or not user.check_password(dto.password.data):
        raise InvalidCredientialException()
    login_user(user)
    return "", 200


def create_public_api_blueprint():
    return public_api_bp


def create_private_api_blueprint():
    private_api_bp = Blueprint("private_api", __name__, url_prefix="/api")
    private_api_bp.register_blueprint(users_api_bp)
    private_api_bp.register_blueprint(requests_api_bp)
    private_api_bp.register_blueprint(skills_api_bp)

    @private_api_bp.before_request
    @login_required
    def require_login():
        pass  # login_required will intercept and redirect unauthenticated user

    return private_api_bp
