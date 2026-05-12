import threading
import os

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from sqlalchemy.pool import StaticPool
from werkzeug.serving import make_server

from app import create_app
from app.extensions import db
from app.models import (
    Request,
    RequestStatus,
    SessionFormat,
    Skill,
    SkillLevel,
    User,
)


@pytest.fixture(scope="session")
def app():
    flask_app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "WTF_CSRF_ENABLED": False,
        "WTF_CSRF_SECRET_KEY": "test-csrf-secret",
        "SQLALCHEMY_DATABASE_URI": "sqlite://",
        "SQLALCHEMY_ENGINE_OPTIONS": {
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
        },
    })

    with flask_app.app_context():
        db.create_all()

    yield flask_app

    with flask_app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(autouse=True)
def clean_database(app):
    with app.app_context():
        db.session.rollback()
        db.session.remove()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()
        yield
        db.session.rollback()
        db.session.remove()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user_factory(app):
    def create_user(
        email="alex@example.com",
        password="password123",
        name="Alex Chen",
    ):
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    return create_user


@pytest.fixture
def skill_factory(app, user_factory):
    def create_skill(user=None, name="Python", level=SkillLevel.INTERMEDIATE):
        user = user or user_factory()
        skill = Skill(
            user_id=user.id,
            name=name,
            level=level,
            description=f"{name} mentoring",
        )
        db.session.add(skill)
        db.session.commit()
        return skill

    return create_skill


@pytest.fixture
def request_factory(app, skill_factory):
    def create_request(owner=None, owner_skill=None, title="Learn guitar"):
        owner_skill = owner_skill or skill_factory(user=owner)
        entity = Request(
            owner_id=owner_skill.user_id,
            owner_skill_id=owner_skill.id,
            skill_to_learn="Guitar",
            status=RequestStatus.OPEN,
            format=SessionFormat.ONLINE,
            title=title,
            description="Looking for beginner lessons.",
            duration="1 hour",
            availability="Weekends",
        )
        db.session.add(entity)
        db.session.commit()
        return entity

    return create_request


@pytest.fixture
def login_user(client, user_factory):
    def login(email="alex@example.com", password="password123"):
        user = user_factory(email=email, password=password)
        response = client.post(
            "/api/login",
            data={"email": email, "password": password},
        )
        assert response.status_code == 200
        return user

    return login


class LiveServer:
    def __init__(self, app):
        self.server = make_server("127.0.0.1", 0, app, threaded=True)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.thread.join(timeout=5)


@pytest.fixture(scope="session")
def server_url(app):
    server = LiveServer(app)
    server.start()
    yield server.url
    server.stop()


@pytest.fixture
def browser():
    options = Options()
    if os.environ.get("SELENIUM_HEADLESS", "1").lower() not in {
        "0",
        "false",
        "no",
    }:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,900")

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as error:
        pytest.skip(f"Chrome WebDriver is not available: {error.msg}")

    yield driver
    driver.quit()
