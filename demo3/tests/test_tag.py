def test_create_tag(client):
    response = client.post("/api/tags", json={"name": "python"})
    assert response.status_code == 201
    assert response.json["name"] == "python"

def test_create_duplicate_tag(client):
    client.post("/api/tags", json={"name": "flask"})
    response = client.post("/api/tags", json={"name": "flask"})
    assert response.status_code == 400
    assert "already exists" in response.json["error"]

def test_list_tags(client):
    client.post("/api/tags", json={"name": "tag1"})
    client.post("/api/tags", json={"name": "tag2"})
    
    response = client.get("/api/tags")
    assert response.status_code == 200
    names = [t["name"] for t in response.json["list"]]
    assert "tag1" in names
    assert "tag2" in names

def test_get_tag(client):
    res = client.post("/api/tags", json={"name": "tag3"})
    tag_id = res.json["id"]
    
    response = client.get(f"/api/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json["name"] == "tag3"

def test_update_tag(client):
    res = client.post("/api/tags", json={"name": "tag4"})
    tag_id = res.json["id"]
    
    response = client.put(f"/api/tags/{tag_id}", json={"name": "tag4-updated"})
    assert response.status_code == 200
    assert response.json["name"] == "tag4-updated"

def test_delete_tag(client):
    res = client.post("/api/tags", json={"name": "tag5"})
    tag_id = res.json["id"]
    
    response = client.delete(f"/api/tags/{tag_id}")
    assert response.status_code == 204
    
    get_res = client.get(f"/api/tags/{tag_id}")
    assert get_res.status_code == 404
