"""Demo3 应用工厂模块。

提供应用创建和初始化功能，实现应用工厂模式。
"""

import logging
import sys
from flask import Flask

from app.extensions import db, migrate
from app.views import register_blueprints
from app.errors import register_error_handlers
from config import config


def configure_logging(app: Flask):
    """配置应用日志。

    Args:
        app: Flask 应用实例
    """
    # 移除默认处理器
    app.logger.handlers.clear()

    # 设置日志级别
    log_level = logging.DEBUG if app.config.get("DEBUG") else logging.INFO
    app.logger.setLevel(log_level)

    # 控制台处理器
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    # 格式化
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)

    # SQLAlchemy 日志（仅调试模式）
    if app.config.get("DEBUG"):
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def create_app(config_name: str) -> Flask:
    """应用工厂函数。

    根据配置名称创建并初始化 Flask 应用。

    Args:
        config_name: 配置名称（develop, test, product）

    Returns:
        配置完成的 Flask 应用实例
    """
    app = Flask(__name__)

    # 配置 JSON 输出：支持中文，保持字段顺序
    app.json.ensure_ascii = False

    # 加载配置
    app.config.from_object(config[config_name])

    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图
    register_blueprints(app)

    # 注册错误处理器
    register_error_handlers(app)

    # 配置日志
    configure_logging(app)

    # 调试配置输出
    if app.config.get("DEBUG"):
        app.logger.debug(
            f"应用已启动，配置: {config_name}\n"
            f"数据库: {app.config.get('SQLALCHEMY_DATABASE_URI')}"
        )

    return app
