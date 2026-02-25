def test_statement_generation(client):
    # Create user
    client.post("/auth/signup", json={
        "email": "stmt@test.com",
        "full_name": "Stmt User",
        "password": "password123"
    })

    login = client.post("/auth/login", data={
        "username": "stmt@test.com",
        "password": "password123"
    })

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create account
    response = client.post("/accounts", json={"currency": "USD"}, headers=headers)
    account_id = response.json()["id"]

    # Deposit
    client.post("/transactions/deposit", json={
        "account_id": account_id,
        "amount": 100
    }, headers=headers)

    # Get statement
    response = client.get(
        f"/statements/account/{account_id}?from_date=2020-01-01T00:00:00&to_date=2030-01-01T00:00:00",
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_credit"] == 100