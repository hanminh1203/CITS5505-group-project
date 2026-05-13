import os
from dotenv import load_dotenv

from app.exceptions import IllegalArgumentException

# Load environment variables from .env file
load_dotenv()


def get_bool_env(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_required(name):
    value = os.environ.get(name)
    if value is None:
        msg = f"Environment variable '{name}' is missing"
        raise IllegalArgumentException(msg)
    return value.strip()


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'sqlite:///database.db',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = get_bool_env('SQLALCHEMY_ECHO', False)
    FLASK_DEBUG = get_bool_env('FLASK_DEBUG', False)
    SECRET_KEY = get_required('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = get_required('WTF_CSRF_SECRET_KEY')
    REQUESTS_PAGE_SIZE = int(os.getenv("REQUESTS_PAGE_SIZE", 6))
