from flask import Flask

from app.config import Config
from app.errors import register_error_handlers
from app.extensions import init_extensions, login_manager
from app.features.api import create_private_api_blueprint, create_public_api_blueprint
from app.features.pages import create_private_views_blueprint, create_public_views_blueprint
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

    flask_app.register_blueprint(create_public_api_blueprint())
    flask_app.register_blueprint(create_private_api_blueprint())
    flask_app.register_blueprint(create_private_views_blueprint())
    flask_app.register_blueprint(create_public_views_blueprint())

    register_error_handlers(flask_app, login_manager)
    return flask_app
