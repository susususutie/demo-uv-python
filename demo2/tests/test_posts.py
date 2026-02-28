"""文章管理 API 测试。"""

import pytest


@pytest.fixture
def sample_post(client, sample_user):
    """创建一个示例文章。"""
    user_id = sample_user["id"]
    response = client.post(
        "/api/posts",
        json={"title": "Test Post", "content": "Test content", "user_id": user_id},
    )
    return response.get_json()


class TestListPosts:
    """测试获取文章列表。"""

    def test_empty_list(self, client):
        """测试空列表。"""
        response = client.get("/api/posts")

        assert response.status_code == 200
        data = response.get_json()
        assert data["list"] == []

    def test_list_with_posts(self, client, sample_post):
        """测试包含文章的列表。"""
        response = client.get("/api/posts")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["list"]) == 1
        assert data["list"][0]["title"] == "Test Post"

    def test_filter_by_user(self, client, sample_user):
        """测试按用户筛选。"""
        # 创建两篇文章
        client.post(
            "/api/posts",
            json={
                "title": "Post 1",
                "content": "Content 1",
                "user_id": sample_user["id"],
            },
        )

        # 创建另一个用户和文章
        resp = client.post(
            "/api/users", json={"username": "other", "email": "other@example.com"}
        )
        other_id = resp.get_json()["id"]
        client.post(
            "/api/posts",
            json={"title": "Post 2", "content": "Content 2", "user_id": other_id},
        )

        # 筛选
        response = client.get(f"/api/posts?user_id={sample_user['id']}")
        data = response.get_json()

        assert len(data["list"]) == 1
        assert data["list"][0]["title"] == "Post 1"

    def test_filter_published(self, client, sample_user):
        """测试只显示已发布文章。"""
        # 创建未发布文章
        client.post(
            "/api/posts",
            json={
                "title": "Draft",
                "content": "Draft content",
                "user_id": sample_user["id"],
                "published": False,
            },
        )

        # 创建已发布文章
        client.post(
            "/api/posts",
            json={
                "title": "Published",
                "content": "Published content",
                "user_id": sample_user["id"],
                "published": True,
            },
        )

        response = client.get("/api/posts?published=true")
        data = response.get_json()

        assert len(data["list"]) == 1
        assert data["list"][0]["title"] == "Published"

    def test_filter_by_keyword_in_title(self, client, sample_user):
        """测试按标题关键词搜索。"""
        # 创建文章
        client.post(
            "/api/posts",
            json={
                "title": "Python Tutorial",
                "content": "Learn Python",
                "user_id": sample_user["id"],
            },
        )
        client.post(
            "/api/posts",
            json={
                "title": "Flask Guide",
                "content": "Learn Flask",
                "user_id": sample_user["id"],
            },
        )

        # 按关键词搜索
        response = client.get("/api/posts?keyword=Python")
        data = response.get_json()

        assert len(data["list"]) == 1
        assert data["list"][0]["title"] == "Python Tutorial"

    def test_filter_by_keyword_in_content(self, client, sample_user):
        """测试按内容关键词搜索。"""
        # 创建文章
        client.post(
            "/api/posts",
            json={
                "title": "Tutorial One",
                "content": "Advanced Python concepts",
                "user_id": sample_user["id"],
            },
        )
        client.post(
            "/api/posts",
            json={
                "title": "Tutorial Two",
                "content": "Basic JavaScript guide",
                "user_id": sample_user["id"],
            },
        )

        # 按内容关键词搜索
        response = client.get("/api/posts?keyword=Python")
        data = response.get_json()

        assert len(data["list"]) == 1
        assert data["list"][0]["title"] == "Tutorial One"


class TestGetPost:
    """测试获取单篇文章。"""

    def test_get_existing(self, client, sample_post):
        """测试获取存在的文章。"""
        post_id = sample_post["id"]
        response = client.get(f"/api/posts/{post_id}")

        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == "Test Post"
        assert "content" in data
        assert "published" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert "user_id" in data

    def test_get_nonexistent(self, client):
        """测试获取不存在的文章。"""
        response = client.get("/api/posts/999")

        assert response.status_code == 404


class TestCreatePost:
    """测试创建文章。"""

    def test_create_success(self, client, sample_user):
        """测试成功创建。"""
        response = client.post(
            "/api/posts",
            json={
                "title": "New Post",
                "content": "New content",
                "user_id": sample_user["id"],
            },
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["title"] == "New Post"
        assert data["published"] is False  # 默认值

    def test_create_with_user_not_found(self, client):
        """测试用户不存在。"""
        response = client.post(
            "/api/posts",
            json={"title": "New Post", "content": "New content", "user_id": 999},
        )

        assert response.status_code == 400

    def test_create_missing_fields(self, client):
        """测试缺少必填字段。"""
        response = client.post("/api/posts", json={"title": "Only Title"})

        assert response.status_code == 400


class TestUpdatePost:
    """测试更新文章。"""

    def test_update_success(self, client, sample_post):
        """测试成功更新。"""
        post_id = sample_post["id"]
        response = client.put(
            f"/api/posts/{post_id}", json={"title": "Updated Title", "published": True}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["title"] == "Updated Title"
        assert data["published"] is True


class TestDeletePost:
    """测试删除文章。"""

    def test_delete_success(self, client, sample_post):
        """测试成功删除，验证返回204无内容状态码。"""
        post_id = sample_post["id"]
        response = client.delete(f"/api/posts/{post_id}")

        # 验证返回 204 No Content
        assert response.status_code == 204
        assert response.data == b""

        # 验证已删除
        get_response = client.get(f"/api/posts/{post_id}")
        assert get_response.status_code == 404
