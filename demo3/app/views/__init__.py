from flask import Flask
from .health import bp as health_bp
from .user import bp as user_bp
from .post import bp as post_bp

# 所有蓝图一次性导出
blueprints = [health_bp, user_bp, post_bp]


def register_blueprints(app: Flask):
    for bp in blueprints:
        app.register_blueprint(bp)
