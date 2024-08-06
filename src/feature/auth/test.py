from src.core.util.test_utilities import get_test_client, TestUser

client = get_test_client(False)


def test_signup():
    data = TestUser.as_dict().copy()
    data.update({"password_confirmation": TestUser.password})
    response = client.post("/auth/signup", json=data)

    print(response.json())

    # Tests whether the new user was created.
    assert response.status_code == 201

    # Test whether authentication data is returned.
    response_json = response.json()
    assert "access_token" in response_json and "refresh_token" in response_json

    # Test if it blocks itself when trying to create a user with an existing email.
    response = client.post("/auth/signup", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered."}


def test_signin():
    response = client.post("/auth/signin", json=TestUser.as_dict())

    response_json = response.json()

    # Test whether authentication data is returned.
    assert response.status_code == 200
    assert "access_token" in response_json and "refresh_token" in response_json

    # Test whether user credentials are invalid.
    response = client.post("/auth/signin", json={"email": "wrong_user@m7academy.com.br", "password": "wrong_password"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Email or password is invalid."}
