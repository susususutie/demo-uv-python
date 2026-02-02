"""Demo2 测试配置和共享固件。

提供测试所需的数据库和应用实例。
"""

import pytest
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 在导入 app 之前设置测试配置环境变量
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app as flask_app, db as _db


@pytest.fixture
def app():
    """创建测试用 Flask 应用。

    使用内存数据库，每次测试后清理数据。
    """
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )

    # 在应用上下文中创建表
    with flask_app.app_context():
        _db.create_all()

    yield flask_app

    # 清理
    with flask_app.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """创建测试客户端。"""
    return app.test_client()


@pytest.fixture
def db(app):
    """提供数据库访问。"""
    with app.app_context():
        yield _db


@pytest.fixture
def sample_user(client):
    """创建一个示例用户，供其他测试使用。

    Returns:
        创建的用户数据字典
    """
    response = client.post(
        "/api/users", json={"username": "testuser", "email": "test@example.com"}
    )
    return response.get_json()
