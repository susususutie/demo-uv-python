import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:  # 公共基类
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-hard-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev.db")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


# 映射字符串 → 配置类
config = {
    "develop": DevelopmentConfig,
    "test": TestingConfig,
    "product": ProductionConfig,
    "default": DevelopmentConfig,
}
