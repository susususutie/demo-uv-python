# app/extensions.py
# 集中声明所有外部扩展实例，避免在 create_app() 之外出现循环导入，内容极少：

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  # 数据库
migrate = Migrate()  # 迁移
