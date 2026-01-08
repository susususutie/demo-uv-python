# app/__init__.py
from flask import Flask
from app.extensions import db, migrate
from app.views import register_blueprints
from config import config


def create_app(config_name):
    app = Flask(__name__)
    app.json.ensure_ascii = False
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    # ===== 调试专用：打印生效配置 =====
    print(">>> ACTIVE CONFIG <<<")
    for k, v in sorted(app.config.items()):
        if k.isupper():  # 只看大写配置项
            print(f"{k}: {v}")
    print(">>> END CONFIG <<<")
    # ===================================

    return app
