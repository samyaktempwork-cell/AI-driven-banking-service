def create_user_and_get_token(client):
    client.post("/auth/signup", json={
        "email": "txn@test.com",
        "full_name": "Txn User",
        "password": "password123"
    })

    response = client.post("/auth/login", data={
        "username": "txn@test.com",
        "password": "password123"
    })

    return response.json()["access_token"]


def test_transaction_flow(client):
    token = create_user_and_get_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create account
    response = client.post("/accounts", json={"currency": "USD"}, headers=headers)
    assert response.status_code == 200
    account_id = response.json()["id"]

    # Deposit
    response = client.post(
        "/transactions/deposit",
        json={"account_id": account_id, "amount": 100},
        headers=headers
    )
    assert response.status_code == 200

    # Withdraw
    response = client.post(
        "/transactions/withdraw",
        json={"account_id": account_id, "amount": 40},
        headers=headers
    )
    assert response.status_code == 200

    # Over-withdraw
    response = client.post(
        "/transactions/withdraw",
        json={"account_id": account_id, "amount": 1000},
        headers=headers
    )
    assert response.status_code == 400