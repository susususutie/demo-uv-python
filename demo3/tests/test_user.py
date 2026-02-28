def test_get_users_empty(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json
    assert data["data"]["list"] == []
    assert data["data"]["pagination"]["total"] == 0


def test_create_user(client):
    response = client.post(
        "/api/users", json={"username": "newuser", "email": "new@example.com"}
    )
    assert response.status_code == 201
    data = response.json["data"]
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data


def test_create_user_duplicate_username(client):
    """测试创建重复用户名的用户。"""
    client.post("/api/users", json={"username": "dupuser", "email": "dup1@example.com"})
    response = client.post(
        "/api/users", json={"username": "dupuser", "email": "dup2@example.com"}
    )
    assert response.status_code == 409
    assert "已存在" in response.json["error"]["message"]


def test_create_user_duplicate_email(client):
    """测试创建重复邮箱的用户。"""
    client.post("/api/users", json={"username": "emailuser1", "email": "same@example.com"})
    response = client.post(
        "/api/users", json={"username": "emailuser2", "email": "same@example.com"}
    )
    assert response.status_code == 409


def test_get_user_detail(client):
    # Create user first
    post_res = client.post(
        "/api/users", json={"username": "detailuser", "email": "detail@example.com"}
    )
    user_id = post_res.json["data"]["id"]

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json["data"]["username"] == "detailuser"


def test_get_user_not_found(client):
    """测试获取不存在的用户。"""
    response = client.get("/api/users/9999")
    assert response.status_code == 404


def test_update_user(client):
    post_res = client.post(
        "/api/users", json={"username": "toupdate", "email": "update@example.com"}
    )
    user_id = post_res.json["data"]["id"]

    response = client.put(
        f"/api/users/{user_id}",
        json={"username": "updated", "email": "update@example.com"},
    )
    assert response.status_code == 200
    assert response.json["data"]["username"] == "updated"


def test_update_user_not_found(client):
    """测试更新不存在的用户。"""
    response = client.put("/api/users/9999", json={"username": "newname"})
    assert response.status_code == 404


def test_update_user_duplicate_username(client):
    """测试更新为已存在的用户名。"""
    # 创建两个用户
    res1 = client.post("/api/users", json={"username": "user1", "email": "u1@example.com"})
    res2 = client.post("/api/users", json={"username": "user2", "email": "u2@example.com"})
    user2_id = res2.json["data"]["id"]

    # 尝试将user2的用户名改为user1
    response = client.put(f"/api/users/{user2_id}", json={"username": "user1"})
    assert response.status_code == 409


def test_delete_user(client):
    post_res = client.post(
        "/api/users", json={"username": "todelete", "email": "delete@example.com"}
    )
    user_id = post_res.json["data"]["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200

    # Verify deleted
    get_res = client.get(f"/api/users/{user_id}")
    assert get_res.status_code == 404


def test_delete_user_not_found(client):
    """测试删除不存在的用户。"""
    response = client.delete("/api/users/9999")
    assert response.status_code == 404


def test_user_list_with_posts_count(client):
    """测试用户列表包含文章数量。"""
    # 创建用户
    res = client.post("/api/users", json={"username": "postcount", "email": "pc@example.com"})
    user_id = res.json["data"]["id"]

    # 创建文章
    for i in range(3):
        client.post(
            "/api/posts",
            json={"title": f"Post {i}", "content": f"Content {i}", "user_id": user_id}
        )

    # 获取用户列表
    response = client.get("/api/users")
    assert response.status_code == 200
    users = response.json["data"]["list"]
    user_data = next(u for u in users if u["username"] == "postcount")
    assert user_data["article_count"] == 3


def test_user_list_keyword_search(client):
    """测试用户列表关键词搜索。"""
    client.post("/api/users", json={"username": "zhangsan", "email": "zhang@example.com"})
    client.post("/api/users", json={"username": "lisi", "email": "lisi@example.com"})

    response = client.get("/api/users?keyword=zhang")
    assert response.status_code == 200
    users = response.json["data"]["list"]
    assert len(users) == 1
    assert users[0]["username"] == "zhangsan"


def test_user_list_username_filter(client):
    """测试用户列表用户名筛选。"""
    client.post("/api/users", json={"username": "filteruser1", "email": "f1@example.com"})
    client.post("/api/users", json={"username": "otheruser", "email": "other@example.com"})

    response = client.get("/api/users?username=filter")
    assert response.status_code == 200
    users = response.json["data"]["list"]
    assert len(users) == 1
    assert users[0]["username"] == "filteruser1"


def test_user_list_sorting(client):
    """测试用户列表排序。"""
    client.post("/api/users", json={"username": "aaa", "email": "aaa@example.com"})
    client.post("/api/users", json={"username": "zzz", "email": "zzz@example.com"})

    # 按用户名升序
    response = client.get("/api/users?sort=username&order=asc")
    users = response.json["data"]["list"]
    usernames = [u["username"] for u in users]
    assert usernames.index("aaa") < usernames.index("zzz")

    # 按用户名降序
    response = client.get("/api/users?sort=username&order=desc")
    users = response.json["data"]["list"]
    usernames = [u["username"] for u in users]
    assert usernames.index("zzz") < usernames.index("aaa")


def test_user_list_pagination(client):
    """测试用户列表分页。"""
    for i in range(5):
        client.post("/api/users", json={"username": f"pageuser{i}", "email": f"pu{i}@example.com"})

    response = client.get("/api/users?per_page=2&page=1")
    data = response.json["data"]
    assert len(data["list"]) == 2
    assert data["pagination"]["total"] == 5
    assert data["pagination"]["pages"] == 3
    assert data["pagination"]["has_next"] is True
