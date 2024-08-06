from src.core.util.test_utilities import get_test_client, TestUser


def teste_me():
    client = get_test_client()
    response = client.get("/users/me")

    assert response.status_code == 200
    assert response.json()['email'] == TestUser.email
