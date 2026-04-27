from flask import Flask

from app.config import Config
from app.errors import register_error_handlers
from app.extensions import init_extensions
from app.features.api import create_api_blueprint
from app.features.pages import create_pages_blueprint
from app.templating import init_template_filters


def create_app():
    flask_app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="../templates",
        static_folder="../static",
    )
    flask_app.config.from_object(Config)

    init_extensions(flask_app)
    init_template_filters(flask_app)

    api_bp = create_api_blueprint()
    views_bp = create_pages_blueprint()
    flask_app.register_blueprint(api_bp)
    flask_app.register_blueprint(views_bp)

    register_error_handlers(flask_app)
    return flask_app
