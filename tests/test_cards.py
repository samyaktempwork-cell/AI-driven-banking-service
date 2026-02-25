def test_issue_and_block_card(client):
    # Create user
    client.post("/auth/signup", json={
        "email": "card@test.com",
        "full_name": "Card User",
        "password": "password123"
    })

    login = client.post("/auth/login", data={
        "username": "card@test.com",
        "password": "password123"
    })

    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create account
    response = client.post("/accounts", json={"currency": "USD"}, headers=headers)
    account_id = response.json()["id"]

    # Issue card
    response = client.post("/cards/", json={
        "account_id": account_id,
        "expiry_date": "2028-12-31",
        "daily_limit": 2000
    }, headers=headers)

    assert response.status_code == 200
    card_id = response.json()["id"]

    # Block card
    response = client.patch(f"/cards/{card_id}/block", headers=headers)
    assert response.status_code == 200