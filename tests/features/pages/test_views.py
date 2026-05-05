def test_home_page_loads(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    assert b"SkillSwap" in response.data
    assert b"Trade what you" in response.data


def test_dashboard_redirects_anonymous_user(client):
    # Arrange
    url = "/dashboard"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
