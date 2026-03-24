import json


def test_change_username(client):

    response = client.post(
        "/user/1/username",
        json={"username": "newname"}
    )

    assert response.status_code == 200

    # check DB actually changed
    res = client.get("/user/1/info")

    data = res.get_json()

    # ❌ test should fail because API is broken
    assert data["users"][0]["username"] == "newname"



def test_change_password(client):

    response = client.post(
        "/user/1/password",
        json={"password": "123456"}
    )

    assert response.status_code == 200

    # ❌ password update is broken
    # we expect failure in logic
    assert False