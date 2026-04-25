from flask import Blueprint

from app.features.requests.api import requests_api_bp
from app.features.users.api import users_api_bp


def create_api_blueprint():
    api_bp = Blueprint("api", __name__, url_prefix="/api")
    api_bp.register_blueprint(users_api_bp)
    api_bp.register_blueprint(requests_api_bp)
    return api_bp