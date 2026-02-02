"""用户管理 API 测试。"""


class TestListUsers:
    """测试获取用户列表。"""

    def test_empty_list(self, client):
        """测试空列表返回。"""
        response = client.get("/api/users")

        assert response.status_code == 200
        data = response.get_json()
        assert data["list"] == []
        assert data["pagination"]["total"] == 0

    def test_list_with_users(self, client, sample_user):
        """测试包含用户的列表。"""
        response = client.get("/api/users")

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["list"]) == 1
        assert data["list"][0]["username"] == "testuser"

    def test_pagination(self, client):
        """测试分页功能。"""
        # 创建多个用户
        for i in range(5):
            client.post(
                "/api/users",
                json={"username": f"user{i}", "email": f"user{i}@example.com"},
            )

        response = client.get("/api/users?per_page=2&page=1")
        data = response.get_json()

        assert len(data["list"]) == 2
        assert data["pagination"]["total"] == 5
        assert data["pagination"]["pages"] == 3
        assert data["pagination"]["has_next"] is True

    def test_keyword_search(self, client):
        """测试关键词搜索。"""
        client.post(
            "/api/users", json={"username": "zhangsan", "email": "zhang@example.com"}
        )
        client.post("/api/users", json={"username": "lisi", "email": "lisi@test.com"})

        response = client.get("/api/users?keyword=zhang")
        data = response.get_json()

        assert len(data["list"]) == 1
        assert data["list"][0]["username"] == "zhangsan"


class TestGetUser:
    """测试获取单个用户。"""

    def test_get_existing_user(self, client, sample_user):
        """测试获取存在的用户。"""
        user_id = sample_user["id"]
        response = client.get(f"/api/users/{user_id}")

        assert response.status_code == 200
        data = response.get_json()
        assert data["username"] == "testuser"
        assert "post_count" in data

    def test_get_nonexistent_user(self, client):
        """测试获取不存在的用户。"""
        response = client.get("/api/users/999")

        assert response.status_code == 404


class TestCreateUser:
    """测试创建用户。"""

    def test_create_success(self, client):
        """测试成功创建用户。"""
        response = client.post(
            "/api/users", json={"username": "newuser", "email": "new@example.com"}
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["username"] == "newuser"
        assert "id" in data
        assert "created_at" in data

    def test_create_duplicate_username(self, client, sample_user):
        """测试重复用户名。"""
        response = client.post(
            "/api/users",
            json={"username": "testuser", "email": "another@example.com"},  # 已存在
        )

        assert response.status_code == 400
        assert "DUPLICATE_USERNAME" in str(response.get_json())

    def test_create_duplicate_email(self, client, sample_user):
        """测试重复邮箱。"""
        response = client.post(
            "/api/users",
            json={"username": "another", "email": "test@example.com"},  # 已存在
        )

        assert response.status_code == 400
        assert "DUPLICATE_EMAIL" in str(response.get_json())

    def test_create_missing_fields(self, client):
        """测试缺少必填字段。"""
        response = client.post("/api/users", json={"username": "onlyname"})

        assert response.status_code == 400


class TestUpdateUser:
    """测试更新用户。"""

    def test_update_success(self, client, sample_user):
        """测试成功更新。"""
        user_id = sample_user["id"]
        response = client.put(
            f"/api/users/{user_id}", json={"username": "updated_name"}
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["username"] == "updated_name"

    def test_update_nonexistent(self, client):
        """测试更新不存在的用户。"""
        response = client.put("/api/users/999", json={"username": "newname"})

        assert response.status_code == 404


class TestDeleteUser:
    """测试删除用户。"""

    def test_delete_success(self, client, sample_user):
        """测试成功删除。"""
        user_id = sample_user["id"]
        response = client.delete(f"/api/users/{user_id}")

        assert response.status_code == 200

        # 验证已删除
        get_response = client.get(f"/api/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent(self, client):
        """测试删除不存在的用户。"""
        response = client.delete("/api/users/999")

        assert response.status_code == 404
