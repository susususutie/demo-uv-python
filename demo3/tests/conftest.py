"""Demo3 测试配置和共享固件。

提供测试所需的数据库和应用实例。
"""

import sys
import os

# 添加 demo3 到 Python 路径，使可以导入 app 包
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import create_app
from app.extensions import db as _db


@pytest.fixture
def app():
    """创建测试用 Flask 应用。

    使用内存数据库，每次测试后清理数据。
    """
    app = create_app("test")

    with app.app_context():
        _db.create_all()
        yield app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def client(app):
    """创建测试客户端。"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """创建 CLI 测试运行器。"""
    return app.test_cli_runner()


@pytest.fixture
def db(app):
    """提供数据库访问。"""
    with app.app_context():
        yield _db
