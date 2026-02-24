def test_full_transaction_flow(client):
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
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Create account
    response = client.post("/accounts", json={"currency": "USD"}, headers=headers)
    assert response.status_code == 200
    account_id = response.json()["id"]

    # Deposit
    response = client.post("/transactions/deposit", json={
        "account_id": account_id,
        "amount": 100
    }, headers=headers)
    assert response.status_code == 200

    # Withdraw
    response = client.post("/transactions/withdraw", json={
        "account_id": account_id,
        "amount": 40
    }, headers=headers)
    assert response.status_code == 200

    # Over-withdraw (should fail)
    response = client.post("/transactions/withdraw", json={
        "account_id": account_id,
        "amount": 1000
    }, headers=headers)
    assert response.status_code == 400