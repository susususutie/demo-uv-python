def test_create_tag(client):
    response = client.post("/api/tags", json={"name": "python"})
    assert response.status_code == 201
    assert response.json["data"]["name"] == "python"


def test_create_duplicate_tag(client):
    client.post("/api/tags", json={"name": "flask"})
    response = client.post("/api/tags", json={"name": "flask"})
    assert response.status_code == 409
    assert "已存在" in response.json["error"]["message"]


def test_list_tags(client):
    client.post("/api/tags", json={"name": "tag1"})
    client.post("/api/tags", json={"name": "tag2"})

    response = client.get("/api/tags")
    assert response.status_code == 200
    names = [t["name"] for t in response.json["data"]["list"]]
    assert "tag1" in names
    assert "tag2" in names


def test_list_tags_name_filter(client):
    """测试标签列表名称筛选。"""
    client.post("/api/tags", json={"name": "python-basic"})
    client.post("/api/tags", json={"name": "javascript"})

    response = client.get("/api/tags?name=python")
    tags = response.json["data"]["list"]
    assert len(tags) == 1
    assert "python" in tags[0]["name"]


def test_list_tags_sorting(client):
    """测试标签列表排序。"""
    client.post("/api/tags", json={"name": "aaa"})
    client.post("/api/tags", json={"name": "zzz"})

    response = client.get("/api/tags?sort=name&order=asc")
    tags = response.json["data"]["list"]
    names = [t["name"] for t in tags]
    assert names.index("aaa") < names.index("zzz")


def test_get_tag(client):
    res = client.post("/api/tags", json={"name": "tag3"})
    tag_id = res.json["data"]["id"]

    response = client.get(f"/api/tags/{tag_id}")
    assert response.status_code == 200
    assert response.json["data"]["name"] == "tag3"


def test_get_tag_not_found(client):
    """测试获取不存在的标签。"""
    response = client.get("/api/tags/9999")
    assert response.status_code == 404


def test_update_tag(client):
    res = client.post("/api/tags", json={"name": "tag4"})
    tag_id = res.json["data"]["id"]

    response = client.put(f"/api/tags/{tag_id}", json={"name": "tag4-updated"})
    assert response.status_code == 200
    assert response.json["data"]["name"] == "tag4-updated"


def test_update_tag_not_found(client):
    """测试更新不存在的标签。"""
    response = client.put("/api/tags/9999", json={"name": "newname"})
    assert response.status_code == 404


def test_update_tag_empty_name(client):
    """测试更新标签时名称为空。"""
    res = client.post("/api/tags", json={"name": "updateme"})
    tag_id = res.json["data"]["id"]

    response = client.put(f"/api/tags/{tag_id}", json={})
    assert response.status_code == 400


def test_update_tag_duplicate_name(client):
    """测试更新为已存在的标签名称。"""
    res1 = client.post("/api/tags", json={"name": "existing1"})
    res2 = client.post("/api/tags", json={"name": "existing2"})
    tag2_id = res2.json["data"]["id"]

    response = client.put(f"/api/tags/{tag2_id}", json={"name": "existing1"})
    assert response.status_code == 409


def test_delete_tag(client):
    res = client.post("/api/tags", json={"name": "tag5"})
    tag_id = res.json["data"]["id"]

    response = client.delete(f"/api/tags/{tag_id}")
    assert response.status_code == 204

    get_res = client.get(f"/api/tags/{tag_id}")
    assert get_res.status_code == 404


def test_delete_tag_not_found(client):
    """测试删除不存在的标签。"""
    response = client.delete("/api/tags/9999")
    assert response.status_code == 404
