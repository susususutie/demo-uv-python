def test_create_post(client):
    # Create user first
    u_res = client.post(
        "/api/users", json={"username": "author", "email": "author@example.com"}
    )
    user_id = u_res.json["data"]["id"]

    response = client.post(
        "/api/posts",
        json={"title": "Test Post", "content": "Content here", "user_id": user_id},
    )
    assert response.status_code == 201
    assert response.json["data"]["title"] == "Test Post"
    assert response.json["data"]["user_id"] == user_id


def test_create_post_user_not_found(client):
    """测试创建文章时用户不存在。"""
    response = client.post(
        "/api/posts",
        json={"title": "Test", "content": "Content", "user_id": 9999},
    )
    assert response.status_code == 404


def test_list_posts(client):
    # Create user and post
    u_res = client.post(
        "/api/users", json={"username": "author2", "email": "author2@example.com"}
    )
    user_id = u_res.json["data"]["id"]
    client.post("/api/posts", json={"title": "P1", "content": "C1", "user_id": user_id})

    response = client.get("/api/posts")
    assert response.status_code == 200
    assert len(response.json["data"]["list"]) >= 1


def test_list_posts_keyword_search(client):
    """测试文章列表关键词搜索。"""
    u_res = client.post("/api/users", json={"username": "kwauthor", "email": "kwa@example.com"})
    user_id = u_res.json["data"]["id"]

    client.post("/api/posts", json={"title": "Python Guide", "content": "Learn Python", "user_id": user_id})
    client.post("/api/posts", json={"title": "Flask Tutorial", "content": "Learn Flask", "user_id": user_id})

    response = client.get("/api/posts?keyword=Python")
    posts = response.json["data"]["list"]
    assert len(posts) == 1
    assert posts[0]["title"] == "Python Guide"


def test_list_posts_title_filter(client):
    """测试文章列表标题筛选。"""
    u_res = client.post("/api/users", json={"username": "tauthor", "email": "ta@example.com"})
    user_id = u_res.json["data"]["id"]

    client.post("/api/posts", json={"title": "Important Topic", "content": "C1", "user_id": user_id})
    client.post("/api/posts", json={"title": "Other Subject", "content": "C2", "user_id": user_id})

    response = client.get("/api/posts?title=Important")
    posts = response.json["data"]["list"]
    assert len(posts) == 1
    assert "Important" in posts[0]["title"]


def test_list_posts_published_filter(client):
    """测试文章列表发布状态筛选。"""
    u_res = client.post("/api/users", json={"username": "pubauthor", "email": "pa@example.com"})
    user_id = u_res.json["data"]["id"]

    client.post("/api/posts", json={"title": "Draft Post", "content": "C1", "user_id": user_id, "published": False})
    client.post("/api/posts", json={"title": "Published Post", "content": "C2", "user_id": user_id, "published": True})

    response = client.get("/api/posts?published=true")
    posts = response.json["data"]["list"]
    assert len(posts) == 1
    assert posts[0]["title"] == "Published Post"
    assert posts[0]["published"] is True


def test_list_posts_sorting(client):
    """测试文章列表排序。"""
    u_res = client.post("/api/users", json={"username": "sortauthor", "email": "sa@example.com"})
    user_id = u_res.json["data"]["id"]

    client.post("/api/posts", json={"title": "A Title", "content": "C1", "user_id": user_id})
    client.post("/api/posts", json={"title": "Z Title", "content": "C2", "user_id": user_id})

    response = client.get("/api/posts?sort=title&order=asc")
    posts = response.json["data"]["list"]
    titles = [p["title"] for p in posts]
    assert titles.index("A Title") < titles.index("Z Title")


def test_get_post(client):
    u_res = client.post(
        "/api/users", json={"username": "author3", "email": "author3@example.com"}
    )
    user_id = u_res.json["data"]["id"]
    p_res = client.post(
        "/api/posts", json={"title": "P2", "content": "C2", "user_id": user_id}
    )
    post_id = p_res.json["data"]["id"]

    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200
    assert response.json["data"]["title"] == "P2"


def test_get_post_not_found(client):
    """测试获取不存在的文章。"""
    response = client.get("/api/posts/9999")
    assert response.status_code == 404


def test_update_post(client):
    u_res = client.post(
        "/api/users", json={"username": "author4", "email": "author4@example.com"}
    )
    user_id = u_res.json["data"]["id"]
    p_res = client.post(
        "/api/posts", json={"title": "P3", "content": "C3", "user_id": user_id}
    )
    post_id = p_res.json["data"]["id"]

    response = client.put(f"/api/posts/{post_id}", json={"title": "P3 Updated"})
    assert response.status_code == 200
    assert response.json["data"]["title"] == "P3 Updated"


def test_update_post_not_found(client):
    """测试更新不存在的文章。"""
    response = client.put("/api/posts/9999", json={"title": "New Title"})
    assert response.status_code == 404


def test_update_post_published_status(client):
    """测试更新文章发布状态。"""
    u_res = client.post("/api/users", json={"username": "upauthor", "email": "ua@example.com"})
    user_id = u_res.json["data"]["id"]
    p_res = client.post("/api/posts", json={"title": "Draft", "content": "C", "user_id": user_id, "published": False})
    post_id = p_res.json["data"]["id"]

    response = client.put(f"/api/posts/{post_id}", json={"published": True})
    assert response.status_code == 200
    assert response.json["data"]["published"] is True


def test_delete_post(client):
    u_res = client.post(
        "/api/users", json={"username": "author5", "email": "author5@example.com"}
    )
    user_id = u_res.json["data"]["id"]
    p_res = client.post(
        "/api/posts", json={"title": "P4", "content": "C4", "user_id": user_id}
    )
    post_id = p_res.json["data"]["id"]

    response = client.delete(f"/api/posts/{post_id}")
    assert response.status_code == 204

    get_res = client.get(f"/api/posts/{post_id}")
    assert get_res.status_code == 404


def test_delete_post_not_found(client):
    """测试删除不存在的文章。"""
    response = client.delete("/api/posts/9999")
    assert response.status_code == 404
