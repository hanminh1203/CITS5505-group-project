from app.extensions import db
from app.models import Request, RequestStatus


def test_user_can_cancel_own_open_request(
    client,
    login_user,
    skill_factory,
    request_factory,
):
    # Arrange
    user = login_user()
    skill = skill_factory(user=user)
    request = request_factory(owner_skill=skill)

    # Act
    response = client.post(f"/api/requests/{request.id}/cancel")

    # Assert
    assert response.status_code == 200
    db.session.expire_all()
    updated_request = db.session.get(Request, request.id)
    assert updated_request.status == RequestStatus.CANCELLED


def test_user_cannot_cancel_another_users_request(
    client,
    login_user,
    user_factory,
    skill_factory,
    request_factory,
):
    # Arrange
    login_user(email="owner@example.com")
    other_user = user_factory(email="other@example.com")
    other_skill = skill_factory(user=other_user)
    other_request = request_factory(owner_skill=other_skill)

    # Act
    response = client.post(f"/api/requests/{other_request.id}/cancel")

    # Assert
    assert response.status_code == 403
    db.session.expire_all()
    unchanged_request = db.session.get(Request, other_request.id)
    assert unchanged_request.status == RequestStatus.OPEN


def test_open_request_cannot_be_completed(
    client,
    login_user,
    skill_factory,
    request_factory,
):
    # Arrange
    user = login_user()
    skill = skill_factory(user=user)
    request = request_factory(owner_skill=skill)

    # Act
    response = client.post(f"/api/requests/{request.id}/complete")

    # Assert
    assert response.status_code == 400
    db.session.expire_all()
    unchanged_request = db.session.get(Request, request.id)
    assert unchanged_request.status == RequestStatus.OPEN


def test_completed_request_cannot_be_cancelled(
    client,
    login_user,
    skill_factory,
    request_factory,
):
    # Arrange
    user = login_user()
    skill = skill_factory(user=user)
    request = request_factory(owner_skill=skill)
    request.status = RequestStatus.COMPLETED
    db.session.commit()

    # Act
    response = client.post(f"/api/requests/{request.id}/cancel")

    # Assert
    assert response.status_code == 400
    db.session.expire_all()
    unchanged_request = db.session.get(Request, request.id)
    assert unchanged_request.status == RequestStatus.COMPLETED
