def test_user_password_is_hashed_and_checked(user_factory):
    # Arrange
    password = "correct-password"

    # Act
    user = user_factory(password=password)

    # Assert
    assert user.password != password
    assert user.check_password(password)
    assert not user.check_password("wrong-password")


def test_email_is_normalized_before_save(user_factory):
    # Arrange
    email = "  ALEX@Example.COM  "

    # Act
    user = user_factory(email=email)

    # Assert
    assert user.email == "alex@example.com"
