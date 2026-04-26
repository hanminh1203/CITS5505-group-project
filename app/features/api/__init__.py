from flask import Blueprint, request
from flask_login import login_required, login_user

from app.features.requests.api import requests_api_bp
from app.features.users.api import users_api_bp
from app.forms.login import LoginForm
from app.models.user import User

def create_public_api_blueprint():
    public_api_bp = Blueprint("public_api", __name__, url_prefix="/api")
    
    @public_api_bp.route("/login", methods=['POST'])
    def authenticate():
        dto = LoginForm(obj = request.form)
        user = User.query.filter_by(email = dto.email.data).first()
        if not user or not user.check_password(dto.password.data):
            return "", 400 # TODO return error message
        login_user(user)
        return "", 200
    
    return public_api_bp

def create_private_api_blueprint():
    private_api_bp = Blueprint("private_api", __name__, url_prefix="/api")
    private_api_bp.register_blueprint(users_api_bp)
    private_api_bp.register_blueprint(requests_api_bp)
    
    @private_api_bp.before_request
    @login_required
    def require_login():
        pass # login_required will intercept and redirect unauthenticated user
    
    return private_api_bp
