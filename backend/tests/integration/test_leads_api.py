from fastapi import status

def test_create_lead_success(client):
    # Arrange
    payload = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "company": "Acme Corp",
        "phone": "555-0199"
    }

    # Act
    response = client.post("/leads", json=payload)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["email"] == "jane@example.com"
    assert data["company"] == "Acme Corp"
    assert data["phone"] == "555-0199"
    assert data["status"] == "NEW"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_lead_duplicate_email(client):
    # Arrange
    payload1 = {
        "name": "Jane Doe",
        "email": "jane.dup@example.com",
        "company": "Acme Corp"
    }
    payload2 = {
        "name": "Another Jane",
        "email": "jane.dup@example.com",
        "company": "Other Corp"
    }

    # Act
    res1 = client.post("/leads", json=payload1)
    res2 = client.post("/leads", json=payload2)

    # Assert
    assert res1.status_code == status.HTTP_201_CREATED
    assert res2.status_code == status.HTTP_409_CONFLICT
    assert "already registered" in res2.json()["detail"]

def test_get_lead_by_id_success(client):
    # Arrange
    payload = {"name": "Test User", "email": "get@example.com"}
    create_res = client.post("/leads", json=payload)
    lead_id = create_res.json()["id"]

    # Act
    response = client.get(f"/leads/{lead_id}")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == lead_id
    assert data["name"] == "Test User"
    assert data["email"] == "get@example.com"

def test_get_lead_by_id_not_found(client):
    # Act
    response = client.get("/leads/99999")

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()

def test_update_lead_success(client):
    # Arrange
    payload = {"name": "Old Name", "email": "old@example.com", "company": "Old Co"}
    create_res = client.post("/leads", json=payload)
    lead_id = create_res.json()["id"]

    update_payload = {
        "name": "New Name",
        "email": "new@example.com",
        "company": "New Co",
        "status": "QUALIFIED"
    }

    # Act
    response = client.put(f"/leads/{lead_id}", json=update_payload)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == lead_id
    assert data["name"] == "New Name"
    assert data["email"] == "new@example.com"
    assert data["company"] == "New Co"
    assert data["status"] == "QUALIFIED"

def test_update_lead_invalid_status(client):
    # Arrange
    payload = {"name": "Test User", "email": "status@example.com"}
    create_res = client.post("/leads", json=payload)
    lead_id = create_res.json()["id"]

    # Act
    response = client.put(f"/leads/{lead_id}", json={"status": "VIP"})

    # Assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = response.json()["detail"].lower()
    assert "input should be" in detail or "not allowed" in detail

def test_list_leads_with_search_and_filter(client):
    # Arrange
    client.post("/leads", json={"name": "Acme Corporation", "email": "acme@example.com", "company": "Acme"})
    client.post("/leads", json={"name": "Initech Soft", "email": "ini@example.com", "company": "Initech"})
    
    # We update one to QUALIFIED to test status filtering
    res = client.post("/leads", json={"name": "Cyberdyne Systems", "email": "cyber@example.com", "company": "Cyberdyne"})
    lead_id = res.json()["id"]
    client.put(f"/leads/{lead_id}", json={"status": "QUALIFIED"})

    # Act 1: Search by text ILIKE on name
    res_search = client.get("/leads?query=corporation")
    # Assert 1
    assert res_search.status_code == status.HTTP_200_OK
    data_search = res_search.json()["leads"]
    assert len(data_search) == 1
    assert data_search[0]["name"] == "Acme Corporation"

    # Act 2: Search by status
    res_status = client.get("/leads?status=QUALIFIED")
    # Assert 2
    assert res_status.status_code == status.HTTP_200_OK
    data_status = res_status.json()["leads"]
    assert len(data_status) == 1
    assert data_status[0]["name"] == "Cyberdyne Systems"

def test_delete_lead_success(client):
    # Arrange
    payload = {"name": "To Delete", "email": "delete@example.com"}
    create_res = client.post("/leads", json=payload)
    lead_id = create_res.json()["id"]

    # Act 1: Delete physical
    del_res = client.delete(f"/leads/{lead_id}")
    # Assert 1
    assert del_res.status_code == status.HTTP_204_NO_CONTENT

    # Act 2: Try to retrieve deleted lead
    get_res = client.get(f"/leads/{lead_id}")
    # Assert 2
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
