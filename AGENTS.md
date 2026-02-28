# Demo UV Python - Agent Guide

## 项目概述

这是一个面向 Python 初学者的 API 开发入门教学项目，通过三个循序渐进的 Demo 演示 Flask API 开发的最佳实践：

- **demo1**: 基础 Flask API（内存存储）
- **demo2**: 数据库版 API（单文件，SQLAlchemy）
- **demo3**: 生产级模块化 API（应用工厂、蓝图、迁移、数据验证）

## 项目结构

```
demo-uv-python/
├── demo1/                 # 基础示例
│   ├── app.py            # 主应用文件
│   ├── README.md         # Demo1 说明文档
│   └── tests/            # 测试文件
│       ├── conftest.py
│       └── test_app.py
├── demo2/                 # 数据库示例
│   ├── app.py            # 主应用文件
│   ├── README.md         # Demo2 说明文档
│   ├── instance/         # 数据库文件目录
│   └── tests/            # 测试文件
│       ├── conftest.py
│       ├── test_health.py
│       ├── test_posts.py
│       └── test_users.py
├── demo3/                 # 生产级示例
│   ├── app/              # 应用包
│   │   ├── __init__.py   # 应用工厂
│   │   ├── models.py     # 数据模型（User, Post, Tag）
│   │   ├── schemas.py    # Marshmallow 序列化模式
│   │   ├── utils.py      # 工具函数
│   │   ├── errors.py     # 错误处理
│   │   ├── responses.py  # 统一响应格式
│   │   ├── extensions.py # 扩展实例（db, migrate）
│   │   └── views/        # 视图/路由（蓝图）
│   │       ├── __init__.py
│   │       ├── endpoints.py  # API 端点列表
│   │       ├── health.py     # 健康检查
│   │       ├── user.py       # 用户管理
│   │       ├── post.py       # 文章管理
│   │       └── tag.py        # 标签管理
│   ├── config.py         # 配置文件
│   ├── run.py            # 启动脚本
│   ├── tests/            # 测试文件
│   │   ├── conftest.py
│   │   ├── test_models.py
│   │   ├── test_user.py
│   │   ├── test_post.py
│   │   ├── test_tag.py
│   │   ├── test_health.py
│   │   └── test_endpoints.py
│   └── migrations/       # 数据库迁移（Alembic）
├── scripts/              # 工具脚本
│   └── batch-insert.py   # 批量数据生成脚本
├── pyproject.toml       # UV 项目配置
├── uv.lock              # 依赖锁定文件
├── README.md            # 主文档
└── AGENTS.md            # 本文件
```

## 工具链与选型说明

### 核心工具：UV

本项目使用 [UV](https://docs.astral.sh/uv/) 作为唯一的 Python 项目管理工具。

**为什么选择 UV？**

1. **极速体验**：Rust 编写，比 pip 快 10-100 倍
2. **一体化**：替代 pip + virtualenv + pip-tools + poetry
3. **锁定文件**：`uv.lock` 确保所有环境一致
4. **原生支持**：无需额外工具即可运行脚本

**常用 UV 命令**：

```bash
# 安装依赖
uv sync                    # 安装生产依赖
uv sync --group dev       # 包含开发依赖

# 运行 Python 脚本
uv run python script.py
uv run demo1/app.py       # 运行 Demo1

# 运行工具
uv run pytest             # 运行测试
uv run black .            # 格式化代码
uv run flask --version    # 运行 Flask CLI
```

### 命令管理方案选型

本项目采用**原生 UV 命令**运行，**不使用 Makefile、Taskipy 或 Poe**。

#### 方案对比

| 方案 | 配置位置 | 优点 | 缺点 | 本项目选择 |
|------|----------|------|------|------------|
| **Makefile** | `Makefile` | 通用、历史悠久 | 语法古老、Windows 需额外安装 | ❌ |
| **Taskipy** | `pyproject.toml` | 轻量、与 UV 配合好 | 额外依赖 | ❌ |
| **Poe the Poet** | `pyproject.toml` | 功能丰富、任务依赖 | 额外依赖、配置稍复杂 | ❌ |
| **Just** | `Justfile` | 现代语法、跨平台 | 额外安装、非 Python 原生 | ❌ |
| **原生 UV** | 无 | 零额外依赖、简单直接 | 命令稍长 | ✅ |

#### 为什么选择原生 UV？

对于本教学项目，选择原生 UV 命令基于以下考量：

**1. 教学友好性**
- 初学者只需学习 UV 一个工具
- 无需理解 Makefile 的 Tab 缩进规则
- 无需学习 Taskipy/Poe 的配置语法
- 命令直接可见，无封装黑盒

**2. 依赖最小化**
- 零额外依赖（仅需 UV）
- 避免工具链过于复杂
- 降低环境配置门槛

**3. 透明直接**
- 便于理解每个命令的具体作用
- 调试更方便
- 无隐藏逻辑

**4. 未来可迁移**
- 当项目复杂化时，可随时引入 Taskipy/Poe
- 迁移成本极低（只需添加配置）

**示例对比**：

```bash
# 原生 UV（当前）
uv run pytest demo1/tests -v

# Taskipy（未来可选）
# 配置: [tool.taskipy.tasks] test-demo1 = "pytest demo1/tests -v"
# 运行: uv run task test-demo1

# Makefile（传统）
# make test-demo1
```

#### 何时应该引入 Taskipy/Poe？

当项目出现以下情况时，建议迁移到任务运行器：

- 命令数量超过 10 个，记忆困难
- 存在复杂的命令依赖链（如 `test` 依赖 `lint`）
- 需要频繁切换不同参数运行同一命令
- 团队成员对长命令感到困扰

### 依赖管理

生产依赖：
```toml
dependencies = [
    "flask>=3.1.2",
    "flask-sqlalchemy>=3.1.1",
    "flask-migrate>=4.1.0",    # 数据库迁移
    "marshmallow>=4.2.0",      # 数据序列化/验证
    "black>=25.12.0",          # 代码格式化
]
```

开发依赖：
```toml
[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "pytest-flask>=1.3.0",
    "pytest-cov>=6.0.0",       # 测试覆盖率
    "httpx>=0.28.1",           # HTTP 客户端（测试和脚本）
]
```

### 数据验证：Marshmallow

Demo3 使用 Marshmallow 进行数据序列化和验证：

```python
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=validate.Length(min=1, max=80))
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)
```

**优势**：
- 声明式 schema 定义
- 自动数据验证
- 序列化/反序列化一体化
- 与 Flask 集成良好

## 代码规范

### Python 风格

- **格式化**：Black（行长度 88）
- **类型注解**：Python 3.9+ 内置类型（`list[str]` 而非 `List[str]`）
- **文档字符串**：Google Style

### 文档字符串格式

```python
def function_name(param1: str, param2: int) -> dict:
    """简短描述。

    详细描述（如果需要）。

    Args:
        param1: 参数1的描述
        param2: 参数2的描述

    Returns:
        返回值的描述

    Raises:
        ValueError: 异常描述

    Example:
        >>> result = function_name("test", 123)
        >>> print(result)
    """
```

### API 响应格式

成功响应：
```json
{
    "data": { ... },
    "message": "操作成功"
}
```

列表响应：
```json
{
    "list": [ ... ],
    "pagination": {
        "page": 1,
        "per_page": 10,
        "total": 100,
        "pages": 10,
        "has_prev": false,
        "has_next": true
    }
}
```

错误响应：
```json
{
    "error": {
        "code": "RESOURCE_NOT_FOUND",
        "message": "用户不存在",
        "details": { ... }
    }
}
```

## 开发流程

### 添加新功能

1. 更新数据模型（`demo3/app/models.py`）
2. 更新序列化模式（`demo3/app/schemas.py`）
3. 实现视图函数（`demo3/app/views/`）
4. 添加测试用例（`demo3/tests/`）
5. 生成数据库迁移（如需要）
6. 更新文档

### 数据库迁移（demo3）

使用原生 UV 命令：

```bash
# 初始化迁移（首次）
cd demo3 && uv run flask --app "app:create_app('develop')" db init

# 生成迁移脚本
cd demo3 && uv run flask --app "app:create_app('develop')" db migrate -m "描述信息"

# 应用迁移
cd demo3 && uv run flask --app "app:create_app('develop')" db upgrade

# 查看历史
cd demo3 && uv run flask --app "app:create_app('develop')" db history

# 回滚到上一个版本
cd demo3 && uv run flask --app "app:create_app('develop')" db downgrade
```

## 常用命令速查

### 开发

```bash
# 运行示例
uv run demo1/app.py
uv run demo2/app.py  # 或 cd demo2 && uv run app.py
uv run demo3/run.py  # 或 cd demo3 && uv run run.py

# 安装依赖
uv sync
uv sync --group dev
```

### 测试

```bash
# 分别运行各示例测试（推荐，避免模块名冲突）
uv run pytest demo1/tests -v
uv run pytest demo2/tests -v
uv run pytest demo3/tests -v

# 生成覆盖率报告
uv run pytest demo1/tests --cov=demo1 --cov-report=html
uv run pytest demo2/tests --cov=demo2 --cov-report=html
uv run pytest demo3/tests --cov=app --cov-report=html

# 查看 HTML 报告
open htmlcov/index.html  # macOS
```

### 代码质量

```bash
# 格式化代码
uv run black demo1/ demo2/ demo3/ --line-length 88

# 语法检查
uv run python -m py_compile demo1/app.py demo2/app.py demo3/run.py

# 清理缓存文件
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
find . -type f -name '*.pyc' -delete 2>/dev/null || true
```

### 数据库

```bash
# Demo3 数据库迁移
cd demo3 && uv run flask --app "app:create_app('develop')" db init
cd demo3 && uv run flask --app "app:create_app('develop')" db migrate -m "描述"
cd demo3 && uv run flask --app "app:create_app('develop')" db upgrade
```

### 数据生成

```bash
# 批量生成测试数据（需要服务运行在 127.0.0.1:3000）
uv run scripts/batch-insert.py --users 10 --posts 5
```

脚本使用 [PEP 723](https://peps.python.org/pep-0723/) 内联依赖声明：
```python
#!/usr/bin/env uv run
# /// script
# dependencies = ["httpx"]
# ///
```

## 功能特性对比

| 特性 | Demo1 | Demo2 | Demo3 |
|------|-------|-------|-------|
| 存储方式 | 内存 | SQLite | SQLite |
| 数据持久化 | ❌ | ✅ | ✅ |
| ORM | ❌ | SQLAlchemy | SQLAlchemy |
| 代码结构 | 单文件 | 单文件 | 模块化 |
| 应用工厂 | ❌ | ❌ | ✅ |
| 蓝图路由 | ❌ | ❌ | ✅ |
| 数据验证 | 手动 | 手动 | Marshmallow |
| 数据库迁移 | ❌ | ❌ | ✅ |
| 错误处理 | 简单 | 结构化 | 完整异常类 |
| 日志配置 | ❌ | ❌ | ✅ |
| API 端点列表 | ❌ | ❌ | ✅ |
| 标签系统 | ❌ | ❌ | ✅ |
| 测试覆盖 | ✅ | ✅ | ✅ |
| 生产就绪 | ❌ | ❌ | ✅ |

## 注意事项

1. **渐进式教学**：保持三个 demo 的递进关系，每个 demo 在前一个基础上增加新概念
2. **中文支持**：所有 JSON 响应需要设置 `ensure_ascii=False`
3. **错误处理**：统一错误响应格式，包含错误码和详细信息
4. **测试覆盖**：核心功能必须有测试覆盖
5. **依赖最小化**：面向初学者，避免引入过多工具链
6. **原生 UV**：所有命令使用 `uv run` 直接运行，不引入额外工具
7. **类型注解**：使用 Python 3.9+ 内置泛型类型（如 `list[str]` 而非 `typing.List[str]`）

## API 使用示例

启动任意 Demo 后，可以使用以下命令测试 API：

```bash
# 健康检查
curl http://127.0.0.1:3000/health

# 获取 API 端点列表（仅 Demo3）
curl http://127.0.0.1:3000/api/endpoints

# 创建用户
curl -X POST http://127.0.0.1:3000/api/users \
    -H "Content-Type: application/json" \
    -d '{"username": "张三", "email": "zhangsan@example.com"}'

# 获取用户列表（分页）
curl "http://127.0.0.1:3000/api/users?page=1&per_page=5"

# 搜索用户
curl "http://127.0.0.1:3000/api/users?keyword=zhang"

# 创建文章
curl -X POST http://127.0.0.1:3000/api/posts \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "title": "第一篇文章", "content": "内容..."}'

# 获取已发布文章
curl "http://127.0.0.1:3000/api/posts?published=true"

# 创建标签（仅 Demo3）
curl -X POST http://127.0.0.1:3000/api/tags \
    -H "Content-Type: application/json" \
    -d '{"name": "技术"}'
```

## 环境变量

```bash
# 配置环境（develop/test/product）
export FLASK_CONFIG=develop

# 数据库 URL（生产环境）
export DATABASE_URL=postgresql://user:pass@localhost/dbname

# 密钥（生产环境必需）
export SECRET_KEY=your-secret-key
```

## 学习路径建议

### 初学者路径

1. **Demo1**：理解 Flask 基础概念
   - 路由定义
   - 请求处理
   - JSON 响应

2. **Demo2**：学习数据库操作
   - SQLAlchemy ORM
   - 数据模型定义
   - 关联关系
   - 分页查询

3. **Demo3**：掌握生产级架构
   - 应用工厂
   - 蓝图组织
   - 数据库迁移
   - 数据验证
   - 日志配置

### 进阶学习

- 阅读各 Demo 的 README.md 了解详细说明
- 查看测试文件学习测试编写
- 研究错误处理和日志配置
- 分析 Marshmallow schema 的使用