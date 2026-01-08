# run.py
# 选配置 → 创建应用 → 启动服务

import os
from app import create_app
from app.models import db

# 优先用环境变量 FLASK_CONFIG，否则默认 develop
config_name = os.getenv("FLASK_CONFIG", "develop")

app = create_app(config_name)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=3000, debug=True)
