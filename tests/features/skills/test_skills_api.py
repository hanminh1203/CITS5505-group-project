from app.extensions import db
from app.models import Skill, SkillLevel


def test_authenticated_user_can_add_skill(client, login_user):
    # Arrange
    user = login_user()
    payload = {
        "name": "Data analysis",
        "level": SkillLevel.ADVANCED.value,
        "description": "Pandas and charts",
    }

    # Act
    response = client.post("/api/skills/", data=payload)

    # Assert
    assert response.status_code == 200
    skill = db.session.get(Skill, response.get_json()["id"])
    assert skill.user_id == user.id
    assert skill.name == payload["name"]
    assert skill.level == SkillLevel.ADVANCED


def test_add_skill_rejects_short_name(client, login_user):
    # Arrange
    login_user()
    payload = {
        "name": "A",
        "level": SkillLevel.BEGINNER.value,
        "description": "Too short",
    }

    # Act
    response = client.post("/api/skills/", data=payload)

    # Assert
    assert response.status_code == 400
    assert Skill.query.count() == 0


def test_add_skill_rejects_invalid_level(client, login_user):
    # Arrange
    login_user()
    payload = {
        "name": "Gardening",
        "level": "Wizard",
        "description": "Balcony herbs",
    }

    # Act
    response = client.post("/api/skills/", data=payload)

    # Assert
    assert response.status_code == 400
    assert Skill.query.count() == 0


def test_user_can_update_own_skill(client, login_user, skill_factory):
    # Arrange
    user = login_user()
    skill = skill_factory(user=user, name="Python")
    payload = {
        "name": "Advanced Python",
        "level": SkillLevel.EXPERT.value,
        "description": "Testing and architecture",
    }

    # Act
    response = client.post(f"/api/skills/{skill.id}", data=payload)

    # Assert
    assert response.status_code == 200
    db.session.expire_all()
    updated_skill = db.session.get(Skill, skill.id)
    assert updated_skill.name == payload["name"]
    assert updated_skill.level == SkillLevel.EXPERT
    assert updated_skill.description == payload["description"]


def test_user_cannot_update_another_users_skill(
    client,
    login_user,
    user_factory,
    skill_factory,
):
    # Arrange
    login_user(email="owner@example.com")
    other_user = user_factory(email="other@example.com")
    other_skill = skill_factory(user=other_user, name="Spanish")
    payload = {
        "name": "French",
        "level": SkillLevel.ADVANCED.value,
        "description": "Attempted overwrite",
    }

    # Act
    response = client.post(f"/api/skills/{other_skill.id}", data=payload)

    # Assert
    assert response.status_code == 403
    db.session.expire_all()
    unchanged_skill = db.session.get(Skill, other_skill.id)
    assert unchanged_skill.name == "Spanish"


def test_user_can_delete_own_skill(client, login_user, skill_factory):
    # Arrange
    user = login_user()
    skill = skill_factory(user=user, name="Photography")

    # Act
    response = client.delete(f"/api/skills/{skill.id}")

    # Assert
    assert response.status_code == 200
    assert db.session.get(Skill, skill.id) is None


def test_user_cannot_delete_another_users_skill(
    client,
    login_user,
    user_factory,
    skill_factory,
):
    # Arrange
    login_user(email="owner@example.com")
    other_user = user_factory(email="other@example.com")
    other_skill = skill_factory(user=other_user, name="Guitar")

    # Act
    response = client.delete(f"/api/skills/{other_skill.id}")

    # Assert
    assert response.status_code == 403
    assert db.session.get(Skill, other_skill.id) is not None
