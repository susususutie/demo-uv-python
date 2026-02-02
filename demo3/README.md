# Demo3: 生产级模块化 Flask API

本示例演示生产级别的 Flask REST API 架构设计，采用模块化组织方式，适合大型项目开发。

## 学习目标

- 理解 Flask 应用工厂模式
- 掌握蓝图（Blueprint）组织路由
- 学习数据库迁移（Flask-Migrate）
- 了解完整的错误处理机制
- 掌握统一的 API 响应格式

## 架构特点

- **应用工厂模式**：动态创建应用实例，支持不同环境配置
- **模块化设计**：功能按模块划分，代码结构清晰
- **蓝图路由**：路由分层管理，便于维护
- **数据库迁移**：使用 Alembic 管理数据库版本
- **完整测试覆盖**：单元测试和集成测试

## 项目结构

```
demo3/
├── app/                    # 应用包
│   ├── __init__.py        # 应用工厂
│   ├── extensions.py      # 扩展实例（db, migrate）
│   ├── models.py          # 数据模型
│   ├── schemas.py         # Marshmallow 序列化模式
│   ├── utils.py           # 工具函数
│   ├── responses.py       # 统一响应格式
│   ├── errors.py          # 错误处理
│   └── views/             # 视图/路由模块
│       ├── __init__.py
│       ├── health.py      # 健康检查
│       ├── user.py        # 用户管理
│       ├── post.py        # 文章管理
│       ├── tag.py         # 标签管理
│       └── endpoints.py   # 端点列表
├── tests/                 # 测试目录
│   ├── conftest.py        # 测试配置
│   ├── test_health.py
│   ├── test_user.py
│   ├── test_post.py
│   ├── test_tag.py
│   ├── test_models.py
│   └── test_endpoints.py
├── migrations/            # 数据库迁移文件
├── config.py             # 环境配置
├── run.py                # 启动脚本
└── README.md
```

## 核心模块说明

### 1. 应用工厂（app/__init__.py）

使用工厂模式创建应用，支持不同环境的配置：

```python
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # 初始化扩展、注册蓝图...
    return app
```

### 2. 数据模型（app/models.py）

定义核心数据模型：

- **User**: 用户表
- **Post**: 文章表
- **Tag**: 标签表

使用混入类（Mixin）共享通用字段（created_at, updated_at）。

### 3. 序列化模式（app/schemas.py）

使用 Marshmallow 进行数据验证和序列化：

```python
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=2, max=80))
    email = fields.Email(required=True)
```

### 4. 统一响应（app/responses.py）

标准化的 API 响应格式：

```python
# 成功响应
{
    "data": { ... },
    "message": "操作成功"
}

# 列表响应
{
    "list": [ ... ],
    "pagination": { ... },
    "message": "获取成功"
}

# 错误响应
{
    "error": {
        "code": "ERROR_CODE",
        "message": "错误描述",
        "details": { ... }  # 可选
    }
}
```

### 5. 错误处理（app/errors.py）

自定义异常类和全局错误处理器：

- `APIError`: 基础 API 错误
- `NotFoundError`: 资源不存在（404）
- `ValidationError`: 数据验证失败（400）
- `DuplicateError`: 数据重复（409）

## 运行应用

```bash
cd demo3 && uv run run.py
```

## 配置说明

在 `config.py` 中定义了三种配置：

| 配置名 | 用途 | 数据库 |
|--------|------|--------|
| develop | 开发环境 | SQLite 文件 |
| test | 测试环境 | SQLite 内存 |
| product | 生产环境 | 环境变量指定 |

切换配置：

```bash
# 通过环境变量
FLASK_CONFIG=product uv run run.py
```

## 数据库迁移

```bash
# 初始化（首次）
cd demo3 && uv run flask --app "app:create_app('develop')" db init

# 创建迁移脚本
cd demo3 && uv run flask --app "app:create_app('develop')" db migrate -m "描述信息"

# 应用迁移
cd demo3 && uv run flask --app "app:create_app('develop')" db upgrade
```

### 回滚迁移

```bash
uv run flask --app "app:create_app('develop')" db downgrade
```

## 测试

```bash
# 运行所有测试
PYTHONPATH=demo3 uv run pytest demo3/tests -v

# 或只运行 Demo3 测试
PYTHONPATH=demo3 uv run pytest demo3/tests -v

# 带覆盖率
PYTHONPATH=demo3 uv run pytest demo3/tests --cov=app --cov-report=html
```

## API 端点

### 系统

- `GET /health` - 健康检查
- `GET /api/endpoints` - 列出所有端点

### 用户

- `GET /api/users` - 用户列表
- `POST /api/users` - 创建用户
- `GET /api/users/<id>` - 用户详情
- `PUT /api/users/<id>` - 更新用户
- `DELETE /api/users/<id>` - 删除用户

### 文章

- `GET /api/posts` - 文章列表
- `POST /api/posts` - 创建文章
- `GET /api/posts/<id>` - 文章详情
- `PUT /api/posts/<id>` - 更新文章
- `DELETE /api/posts/<id>` - 删除文章

### 标签

- `GET /api/tags` - 标签列表
- `POST /api/tags` - 创建标签
- `GET /api/tags/<id>` - 标签详情
- `PUT /api/tags/<id>` - 更新标签
- `DELETE /api/tags/<id>` - 删除标签

## 与 Demo2 的区别

| 特性 | Demo2 | Demo3 |
|------|-------|-------|
| 代码组织 | 单文件 | 模块化包 |
| 应用创建 | 全局实例 | 应用工厂 |
| 路由组织 | 直接注册 | 蓝图 |
| 数据库迁移 | ❌ | ✅ |
| 错误处理 | 简单 | 完整异常类 |
| 响应格式 | 基本 JSON | 统一标准格式 |
| 日志配置 | 默认 | 结构化配置 |
| 生产就绪 | ❌ | ✅ |

## 扩展阅读

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Marshmallow](https://marshmallow.readthedocs.io/)
