"""健康检查端点测试。"""


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
