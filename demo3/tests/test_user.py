def test_get_users_empty(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert response.json["list"] == []
    assert response.json["pagination"]["total"] == 0

def test_create_user(client):
    response = client.post("/api/users", json={
        "username": "newuser",
        "email": "new@example.com"
    })
    assert response.status_code == 201
    data = response.json
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data

def test_get_user_detail(client):
    # Create user first
    post_res = client.post("/api/users", json={
        "username": "detailuser",
        "email": "detail@example.com"
    })
    user_id = post_res.json["id"]
    
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json["username"] == "detailuser"

def test_update_user(client):
    post_res = client.post("/api/users", json={
        "username": "toupdate",
        "email": "update@example.com"
    })
    user_id = post_res.json["id"]
    
    response = client.put(f"/api/users/{user_id}", json={
        "username": "updated",
        "email": "update@example.com"
    })
    assert response.status_code == 200
    assert response.json["username"] == "updated"

def test_delete_user(client):
    post_res = client.post("/api/users", json={
        "username": "todelete",
        "email": "delete@example.com"
    })
    user_id = post_res.json["id"]
    
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    
    # Verify deleted
    get_res = client.get(f"/api/users/{user_id}")
    assert get_res.status_code == 404
