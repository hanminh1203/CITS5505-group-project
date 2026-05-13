def test_login_api_accepts_valid_credentials(client, user_factory):
    # Arrange
    email = "login@example.com"
    password = "password123"
    user_factory(email=email, password=password)

    # Act
    response = client.post(
        "/api/login",
        data={"email": email, "password": password},
    )

    # Assert
    assert response.status_code == 200


def test_login_api_rejects_invalid_password(client, user_factory):
    # Arrange
    email = "login@example.com"
    user_factory(email=email, password="password123")

    # Act
    response = client.post(
        "/api/login",
        data={"email": email, "password": "wrong"},
    )

    # Assert
    assert response.status_code == 400


def test_login_api_rejects_unknown_email(client):
    # Arrange
    credentials = {
        "email": "missing@example.com",
        "password": "password123",
    }

    # Act
    response = client.post("/api/login", data=credentials)

    # Assert
    assert response.status_code == 400
