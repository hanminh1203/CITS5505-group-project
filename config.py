import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_bool_env(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = get_bool_env('SQLALCHEMY_ECHO', False)
    FLASK_DEBUG = get_bool_env('FLASK_DEBUG', False)
