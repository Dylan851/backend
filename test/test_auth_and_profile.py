def register_user(client, email="user@example.com", username="tester", password="secret123"):
    return client.post(
        "/auth/register",
        json={
            "email": email,
            "username": username,
            "password": password,
        },
    )


def login_user(client, identifier="user@example.com", password="secret123"):
    return client.post(
        "/auth/login",
        json={
            "identifier": identifier,
            "password": password,
        },
    )


def auth_headers_from_response(response):
    token = response.json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_creates_user_and_player(client):
    response = register_user(client, email="NEWUSER@Example.com", username="nuevo")

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["token"]
    assert payload["player"]["nickname"] == "nuevo"
    assert payload["player"]["level"] == 1
    assert payload["player"]["coins"] == 0


def test_register_normalizes_email_to_lowercase(client):
    register_user(client, email="MixedCase@Example.com", username="mixed")

    methods = client.post("/auth/methods", json={"email": "mixedcase@example.com"})

    assert methods.status_code == 200
    data = methods.json()["data"]
    assert data["email"] == "mixedcase@example.com"
    assert data["exists"] is True


def test_register_rejects_duplicate_email(client):
    register_user(client, email="repeat@example.com", username="uno")

    response = register_user(client, email="repeat@example.com", username="dos")

    assert response.status_code == 400
    assert "ya esta registrado" in response.json()["detail"].lower()


def test_register_rejects_duplicate_username(client):
    register_user(client, email="uno@example.com", username="repetido")

    response = register_user(client, email="dos@example.com", username="repetido")

    assert response.status_code == 400
    assert "nombre de usuario" in response.json()["detail"].lower()


def test_login_with_email_returns_token_and_profile(client):
    register_user(client, email="login@example.com", username="loginuser")

    response = login_user(client, identifier="login@example.com")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["token"]
    assert data["player"]["nickname"] == "loginuser"


def test_login_with_username_works(client):
    register_user(client, email="nick@example.com", username="nicklogin")

    response = login_user(client, identifier="nicklogin")

    assert response.status_code == 200
    assert response.json()["data"]["player"]["nickname"] == "nicklogin"


def test_login_rejects_wrong_password(client):
    register_user(client, email="badpass@example.com", username="badpass")

    response = login_user(client, identifier="badpass@example.com", password="incorrecta")

    assert response.status_code == 401
    assert "incorrectos" in response.json()["detail"].lower()


def test_auth_methods_reports_existing_password_account(client):
    register_user(client, email="methods@example.com", username="methods")

    response = client.post("/auth/methods", json={"email": "methods@example.com"})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["exists"] is True
    assert data["has_password"] is True
    assert data["has_google"] is False


def test_auth_methods_reports_non_existing_account(client):
    response = client.post("/auth/methods", json={"email": "missing@example.com"})

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["exists"] is False
    assert data["has_password"] is False
    assert data["has_google"] is False


def test_password_recovery_returns_generic_message_for_existing_password_user(client):
    register_user(client, email="recover@example.com", username="recover")

    response = client.post("/auth/password/recover", json={"email": "recover@example.com"})

    assert response.status_code == 200
    assert "restablecer" in response.json()["data"]["message"].lower()


def test_password_recovery_returns_generic_message_for_non_existing_user(client):
    response = client.post("/auth/password/recover", json={"email": "nobody@example.com"})

    assert response.status_code == 200
    assert "restablecer" in response.json()["data"]["message"].lower()


def test_profile_requires_authentication(client):
    response = client.get("/player/profile")

    assert response.status_code in {401, 403}


def test_get_profile_returns_registered_player_data(client):
    register_response = register_user(client, email="profile@example.com", username="perfil")

    response = client.get("/player/profile", headers=auth_headers_from_response(register_response))

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["nickname"] == "perfil"
    assert data["level"] == 1
    assert data["coins"] == 0
    assert data["inventory"] == []


def test_update_profile_changes_nickname(client):
    register_response = register_user(client, email="rename@example.com", username="antes")

    response = client.put(
        "/player/profile",
        headers=auth_headers_from_response(register_response),
        json={"nickname": "despues"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["nickname"] == "despues"


def test_update_location_changes_coordinates(client):
    register_response = register_user(client, email="location@example.com", username="mapa")

    response = client.put(
        "/player/location",
        headers=auth_headers_from_response(register_response),
        json={"coord_lat": 40.4168, "coord_lng": -3.7038},
    )

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["coord_lat"] == 40.4168
    assert data["coord_lng"] == -3.7038
