def test_create_post(client):
    # Create user first
    u_res = client.post("/api/users", json={"username": "author", "email": "author@example.com"})
    user_id = u_res.json["id"]
    
    response = client.post("/api/posts", json={
        "title": "Test Post",
        "content": "Content here",
        "user_id": user_id
    })
    assert response.status_code == 201
    assert response.json["title"] == "Test Post"
    assert response.json["user_id"] == user_id

def test_list_posts(client):
    # Create user and post
    u_res = client.post("/api/users", json={"username": "author2", "email": "author2@example.com"})
    user_id = u_res.json["id"]
    client.post("/api/posts", json={"title": "P1", "content": "C1", "user_id": user_id})
    
    response = client.get("/api/posts")
    assert response.status_code == 200
    assert len(response.json["list"]) >= 1

def test_get_post(client):
    u_res = client.post("/api/users", json={"username": "author3", "email": "author3@example.com"})
    user_id = u_res.json["id"]
    p_res = client.post("/api/posts", json={"title": "P2", "content": "C2", "user_id": user_id})
    post_id = p_res.json["id"]
    
    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200
    assert response.json["title"] == "P2"

def test_update_post(client):
    u_res = client.post("/api/users", json={"username": "author4", "email": "author4@example.com"})
    user_id = u_res.json["id"]
    p_res = client.post("/api/posts", json={"title": "P3", "content": "C3", "user_id": user_id})
    post_id = p_res.json["id"]
    
    response = client.put(f"/api/posts/{post_id}", json={"title": "P3 Updated"})
    assert response.status_code == 200
    assert response.json["title"] == "P3 Updated"

def test_delete_post(client):
    u_res = client.post("/api/users", json={"username": "author5", "email": "author5@example.com"})
    user_id = u_res.json["id"]
    p_res = client.post("/api/posts", json={"title": "P4", "content": "C4", "user_id": user_id})
    post_id = p_res.json["id"]
    
    response = client.delete(f"/api/posts/{post_id}")
    assert response.status_code == 204
    
    get_res = client.get(f"/api/posts/{post_id}")
    assert get_res.status_code == 404
