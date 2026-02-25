def test_signup_and_login(client):
    # Signup
    response = client.post("/auth/signup", json={
        "email": "test@test.com",
        "full_name": "Test User",
        "password": "password123"
    })
    assert response.status_code == 200

    # Login
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()