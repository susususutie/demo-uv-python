"""Demo3 视图包。

集中管理所有蓝图注册。
"""

from flask import Flask

from .health import bp as health_bp
from .user import bp as user_bp
from .post import bp as post_bp
from .tag import bp as tag_bp
from .endpoints import bp as endpoints_bp

# 所有蓝图列表
blueprints = [health_bp, user_bp, post_bp, tag_bp, endpoints_bp]


def register_blueprints(app: Flask) -> None:
    """注册所有蓝图到 Flask 应用。

    Args:
        app: Flask 应用实例
    """
    for bp in blueprints:
        app.register_blueprint(bp)
        app.logger.debug(f"已注册蓝图: {bp.name}")
