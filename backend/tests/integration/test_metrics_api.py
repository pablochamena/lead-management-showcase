from fastapi import status

def test_metrics_empty_database_returns_zero(client):
    # Act
    response = client.get("/metrics")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {
        "new": 0,
        "contacted": 0,
        "qualified": 0,
        "lost": 0
    }

def test_metrics_updates_on_lead_creation_and_transitions(client):
    # Arrange: Create leads in different states
    # Lead 1: NEW (created by default)
    res1 = client.post("/leads", json={"name": "Lead 1", "email": "lead1@example.com"})
    
    # Lead 2: CONTACTED
    res2 = client.post("/leads", json={"name": "Lead 2", "email": "lead2@example.com"})
    client.put(f"/leads/{res2.json()['id']}", json={"status": "CONTACTED"})

    # Lead 3: QUALIFIED
    res3 = client.post("/leads", json={"name": "Lead 3", "email": "lead3@example.com"})
    client.put(f"/leads/{res3.json()['id']}", json={"status": "QUALIFIED"})

    # Lead 4: LOST
    res4 = client.post("/leads", json={"name": "Lead 4", "email": "lead4@example.com"})
    client.put(f"/leads/{res4.json()['id']}", json={"status": "LOST"})

    # Lead 5: NEW
    client.post("/leads", json={"name": "Lead 5", "email": "lead5@example.com"})

    # Act
    response = client.get("/metrics")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["new"] == 2
    assert data["contacted"] == 1
    assert data["qualified"] == 1
    assert data["lost"] == 1
