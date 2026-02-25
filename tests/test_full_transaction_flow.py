def test_full_transaction_flow(client):
    # -----------------------------
    # Signup
    # -----------------------------
    response = client.post("/auth/signup", json={
        "email": "test@test.com",
        "full_name": "Test User",
        "password": "password123"
    })
    assert response.status_code == 200

    # -----------------------------
    # Login
    # -----------------------------
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 200

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # -----------------------------
    # Create Account
    # -----------------------------
    response = client.post(
        "/accounts",
        json={"currency": "USD"},
        headers=headers
    )
    assert response.status_code == 200

    account_id = response.json()["id"]

    # -----------------------------
    # Deposit
    # -----------------------------
    response = client.post(
        "/transactions/deposit",
        json={"account_id": account_id, "amount": 100},
        headers=headers
    )
    assert response.status_code == 200

    # -----------------------------
    # Withdraw
    # -----------------------------
    response = client.post(
        "/transactions/withdraw",
        json={"account_id": account_id, "amount": 40},
        headers=headers
    )
    assert response.status_code == 200

    # -----------------------------
    # Over-withdraw (Should Fail)
    # -----------------------------
    response = client.post(
        "/transactions/withdraw",
        json={"account_id": account_id, "amount": 1000},
        headers=headers
    )
    assert response.status_code == 400

    # -----------------------------
    # Issue Card
    # -----------------------------
    response = client.post(
        "/cards/",
        json={
            "account_id": account_id,
            "expiry_date": "2028-12-31",
            "daily_limit": 200
        },
        headers=headers
    )
    assert response.status_code == 200

    card_id = response.json()["id"]

    # -----------------------------
    # Block Card
    # -----------------------------
    response = client.patch(
        f"/cards/{card_id}/block",
        headers=headers
    )
    assert response.status_code == 200

    # -----------------------------
    # List Cards
    # -----------------------------
    response = client.get(
        f"/cards/account/{account_id}",
        headers=headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

    # -----------------------------
    # Get Statement
    # -----------------------------
    response = client.get(
        f"/statements/account/{account_id}?from_date=2020-01-01T00:00:00&to_date=2030-01-01T00:00:00",
        headers=headers
    )
    assert response.status_code == 200

    statement = response.json()

    # Validate totals
    assert statement["total_credit"] == 100
    assert statement["total_debit"] == 40