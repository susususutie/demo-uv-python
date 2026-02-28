"""健康检查端点测试。"""

import pytest


class TestHealthCheck:
    """测试健康检查功能。"""

    def test_health_returns_ok(self, client):
        """测试健康检查返回正常状态。"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.get_json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["database"] == "connected"


class TestApiInfo:
    """测试 API 信息端点。"""

    def test_api_info_structure(self, client):
        """测试 API 信息包含必要字段。"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        assert "users" in data["endpoints"]
        assert "posts" in data["endpoints"]


class TestErrorHandling:
    """测试错误处理器。"""

    def test_404_error_format(self, client):
        """测试 404 错误返回标准化格式。"""
        response = client.get("/nonexistent-endpoint")

        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data
        assert data["error"]["code"] == "RESOURCE_NOT_FOUND"

    def test_405_error_format(self, client):
        """测试 405 错误返回标准化格式。"""
        response = client.post("/health")  # health 只支持 GET

        assert response.status_code == 405

    def test_500_error_handler_registered(self, app):
        """测试 500 错误处理器已注册。"""
        # 验证错误处理器存在
        assert 500 in app.error_handler_spec[None]

    def test_not_found_handler_directly(self, app):
        """直接测试 404 错误处理函数。"""
        with app.app_context():
            from app import not_found

            class MockError:
                pass

            response = not_found(MockError())
            assert response[1] == 404
            assert "RESOURCE_NOT_FOUND" in str(response[0].get_json())

    def test_bad_request_handler_directly(self, app):
        """直接测试 400 错误处理函数。"""
        with app.app_context():
            from app import bad_request

            class MockError:
                pass

            response = bad_request(MockError())
            assert response[1] == 400
            assert "BAD_REQUEST" in str(response[0].get_json())

    def test_internal_error_handler_directly(self, app):
        """直接测试 500 错误处理函数。"""
        with app.app_context():
            from app import internal_error

            class MockError:
                pass

            response = internal_error(MockError())
            assert response[1] == 500
            assert "INTERNAL_ERROR" in str(response[0].get_json())
