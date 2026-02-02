"""Demo1 测试配置和共享固件。

提供测试所需的 Flask 应用和客户端实例。
"""

import sys
import os

# 添加 demo1 到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app as flask_app


@pytest.fixture
def app():
    """创建测试用 Flask 应用实例。

    Returns:
        配置为测试模式的 Flask 应用
    """
    flask_app.config.update(
        {
            "TESTING": True,
        }
    )
    return flask_app


@pytest.fixture
def client(app):
    """创建测试客户端。

    Args:
        app: Flask 应用实例

    Returns:
        可用于发送请求的测试客户端
    """
    return app.test_client()
