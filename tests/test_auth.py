async def test_register_login_and_get_me(client, create_user_and_login):
    auth = await create_user_and_login()

    response = await client.get(
        "/auth/me",
        headers=auth["headers"]
    )

    assert response.status_code == 200
    assert response.json()["email"] == auth["email"]