from server.adapters.database.models import Secret


async def test_get_secrets(test_client, secret_in_db_with_raw_data_and_password):
    secret, data, password = secret_in_db_with_raw_data_and_password
    response = test_client.get(
        f"/secrets/{secret.id}", params={"password": password.decode()}
    )
    assert response.status_code == 200
    assert response.json() == {
        "secret_data": data,
    }


async def test_invalid_password_secrets(
    test_client, secret_in_db_with_raw_data_and_password
):
    secret, data, password = secret_in_db_with_raw_data_and_password
    response = test_client.get(
        f"/secrets/{secret.id}", params={"password": (password + "123").decode()}
    )
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Invalid password for this secret",
    }


async def test_secret_not_found(test_client):
    response = test_client.get(
        f"/secrets/13d12514-52d6-4e1a-977e-b3790e7cf0c9", params={"password": b"123"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Secret was not found",
    }


async def test_generate_secret(test_client, session):
    response = test_client.post(
        "/generate",
        data={
            "secret_data": "some secret data",
            "password": "some password",
        },
    )

    result = response.json()
    key = result["secret_key"]

    secret = await Secret.get(session, id=key)
    assert secret is not None
