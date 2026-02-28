def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json["data"]
    assert data["status"] == "UP"
    assert "timestamp" in data
    assert data["database"] == "connected"


def test_health_check_db_failure(client, app, monkeypatch):
    """测试数据库连接失败时的健康检查。"""
    # 模拟数据库连接失败
    def mock_execute(*args, **kwargs):
        raise Exception("Database connection failed")

    with app.app_context():
        from app.extensions import db

        original_execute = db.session.execute
        db.session.execute = mock_execute

        try:
            response = client.get("/health")
            assert response.status_code == 500
            assert "DATABASE_ERROR" in response.json["error"]["code"]
        finally:
            db.session.execute = original_execute
