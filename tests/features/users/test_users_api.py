def test_private_api_requires_login(client):
    # Arrange
    url = "/api/users/"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 401


def test_users_api_lists_users_in_id_order(client, login_user, user_factory):
    # Arrange
    login_user(email="first@example.com")
    user_factory(email="second@example.com")

    # Act
    response = client.get("/api/users/")

    # Assert
    assert response.status_code == 200
    assert [user["name"] for user in response.get_json()] == [
        "first@example.com",
        "second@example.com",
    ]
