from fastapi import status

def test_register_activity_success(client):
    # Arrange: Create a lead first
    lead_res = client.post("/leads", json={"name": "Alice Lead", "email": "alice@example.com"})
    lead_id = lead_res.json()["id"]

    payload = {
        "type": "CALL",
        "notes": "Spoke to Alice, she is interested."
    }

    # Act
    response = client.post(f"/leads/{lead_id}/activities", json=payload)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["lead_id"] == lead_id
    assert data["type"] == "CALL"
    assert data["notes"] == "Spoke to Alice, she is interested."
    assert "id" in data
    assert "created_at" in data

def test_register_activity_lead_not_found(client):
    # Arrange
    payload = {
        "type": "NOTE",
        "notes": "This will fail"
    }

    # Act
    response = client.post("/leads/99999/activities", json=payload)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()

def test_list_activities_chronological_desc(client):
    # Arrange: Create a lead and register multiple activities
    lead_res = client.post("/leads", json={"name": "Bob Lead", "email": "bob@example.com"})
    lead_id = lead_res.json()["id"]

    client.post(f"/leads/{lead_id}/activities", json={"type": "EMAIL", "notes": "First email"})
    client.post(f"/leads/{lead_id}/activities", json={"type": "CALL", "notes": "Second call"})
    client.post(f"/leads/{lead_id}/activities", json={"type": "NOTE", "notes": "Third note"})

    # Act
    response = client.get(f"/leads/{lead_id}/activities")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    # Check that they are ordered by created_at DESC (latest first)
    assert data[0]["notes"] == "Third note"
    assert data[1]["notes"] == "Second call"
    assert data[2]["notes"] == "First email"

def test_activities_api_immutability(client):
    # Arrange: Create lead and activity
    lead_res = client.post("/leads", json={"name": "Bob Lead", "email": "bob.imm@example.com"})
    lead_id = lead_res.json()["id"]
    act_res = client.post(f"/leads/{lead_id}/activities", json={"type": "EMAIL", "notes": "First email"})
    act_id = act_res.json()["id"]

    # Act & Assert 1: Collection endpoint PUT/DELETE returns 405 Method Not Allowed
    put_coll = client.put(f"/leads/{lead_id}/activities", json={"notes": "Try update"})
    assert put_coll.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    del_coll = client.delete(f"/leads/{lead_id}/activities")
    assert del_coll.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    # Act & Assert 2: Individual endpoint PUT/DELETE returns 404 Not Found (since routes are not declared)
    put_indiv = client.put(f"/leads/{lead_id}/activities/{act_id}", json={"notes": "Try update"})
    assert put_indiv.status_code == status.HTTP_404_NOT_FOUND

    del_indiv = client.delete(f"/leads/{lead_id}/activities/{act_id}")
    assert del_indiv.status_code == status.HTTP_404_NOT_FOUND
