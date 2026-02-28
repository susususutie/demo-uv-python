"""Demo1 应用测试模块。

测试所有 API 端点的功能正确性。
"""

import pytest


class TestRootEndpoint:
    """测试根路径端点。"""

    def test_hello_returns_api_info(self, client):
        """测试首页返回正确的 API 信息。"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert "version" in data
        assert data["demo"] == "基础内存存储版 API"


class TestGetUsers:
    """测试获取用户列表功能。"""

    def test_get_users_returns_list(self, client):
        """测试获取用户列表返回数组。"""
        response = client.get("/users")

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 2  # 初始有 2 个用户

    def test_initial_users_have_required_fields(self, client):
        """测试初始用户数据包含必要字段。"""
        response = client.get("/users")
        data = response.get_json()

        for user in data:
            assert "id" in user
            assert "name" in user
            assert "email" in user


class TestGetUser:
    """测试获取单个用户功能。"""

    def test_get_existing_user(self, client):
        """测试获取存在的用户。"""
        response = client.get("/users/1")

        assert response.status_code == 200
        data = response.get_json()
        assert data["id"] == 1
        assert "name" in data

    def test_get_nonexistent_user_returns_404(self, client):
        """测试获取不存在的用户返回 404。"""
        response = client.get("/users/9999")

        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


class TestCreateUser:
    """测试创建用户功能。"""

    def test_create_user_success(self, client):
        """测试成功创建用户。"""
        response = client.post(
            "/users", json={"name": "测试用户", "email": "test@example.com"}
        )

        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "测试用户"
        assert data["email"] == "test@example.com"
        assert "id" in data

    def test_create_user_without_name_fails(self, client):
        """测试缺少 name 字段时创建失败。"""
        response = client.post("/users", json={"email": "test@example.com"})

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_user_without_email_fails(self, client):
        """测试缺少 email 字段时创建失败。"""
        response = client.post("/users", json={"name": "测试用户"})

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_create_user_with_empty_body_fails(self, client):
        """测试空请求体创建失败。"""
        response = client.post("/users", json={})

        assert response.status_code == 400


class TestUpdateUser:
    """测试更新用户功能。"""

    def test_update_user_name(self, client):
        """测试更新用户名称。"""
        # 先创建一个用户
        create_resp = client.post(
            "/users", json={"name": "原名称", "email": "update@example.com"}
        )
        user_id = create_resp.get_json()["id"]

        # 更新名称
        response = client.put(f"/users/{user_id}", json={"name": "新名称"})

        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "新名称"
        assert data["email"] == "update@example.com"  # 未修改

    def test_update_nonexistent_user_returns_404(self, client):
        """测试更新不存在的用户返回 404。"""
        response = client.put("/users/9999", json={"name": "新名称"})

        assert response.status_code == 404


class TestDeleteUser:
    """测试删除用户功能。"""

    def test_delete_user_success(self, client):
        """测试成功删除用户。"""
        # 先创建一个用户
        create_resp = client.post(
            "/users", json={"name": "待删除", "email": "delete@example.com"}
        )
        user_id = create_resp.get_json()["id"]

        # 删除用户
        response = client.delete(f"/users/{user_id}")

        assert response.status_code == 200

        # 验证已删除
        get_resp = client.get(f"/users/{user_id}")
        assert get_resp.status_code == 404

    def test_delete_nonexistent_user_returns_404(self, client):
        """测试删除不存在的用户返回 404。"""
        response = client.delete("/users/9999")

        assert response.status_code == 404


class TestErrorHandling:
    """测试错误处理。"""

    def test_404_error_format(self, client):
        """测试 404 错误返回 JSON 格式。"""
        response = client.get("/nonexistent-path")

        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_method_not_allowed(self, client):
        """测试不允许的请求方法。"""
        response = client.post("/")  # 根路径只支持 GET

        assert response.status_code == 405
        data = response.get_json()
        assert "error" in data

    def test_internal_error_handler_exists(self, app):
        """测试 500 错误处理器已注册。"""
        # 验证错误处理器已注册
        # 由于 Flask 在 TESTING=True 模式下会直接抛出异常而不是调用错误处理器，
        # 我们只验证处理器存在
        error_handlers = app.error_handler_spec

        # Flask 的错误处理器结构是嵌套字典
        # 500 错误处理器应该在 None 键下（表示全局处理器）
        has_500_handler = False
        for key, spec in error_handlers.items():
            if isinstance(spec, dict) and 500 in spec:
                has_500_handler = True
                break

        assert has_500_handler, "500 错误处理器未注册"

    def test_not_found_handler_directly(self, app):
        """直接测试 404 错误处理函数。"""
        with app.app_context():
            from app import not_found

            class MockError:
                pass

            response = not_found(MockError())
            assert response[1] == 404
            assert "error" in response[0].get_json()

    def test_method_not_allowed_handler_directly(self, app):
        """直接测试 405 错误处理函数。"""
        with app.app_context():
            from app import method_not_allowed

            class MockError:
                pass

            response = method_not_allowed(MockError())
            assert response[1] == 405
            assert "error" in response[0].get_json()

    def test_internal_error_handler_directly(self, app):
        """直接测试 500 错误处理函数。"""
        with app.app_context():
            from app import internal_error

            class MockError:
                pass

            response = internal_error(MockError())
            assert response[1] == 500
            assert "error" in response[0].get_json()
            assert "服务器内部错误" in response[0].get_json()["error"]
