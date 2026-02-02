# Demo UV Python - Python API 开发入门教程

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.x](https://img.shields.io/badge/flask-3.x-green.svg)](https://flask.palletsprojects.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![UV](https://img.shields.io/badge/uv-powered-purple.svg)](https://docs.astral.sh/uv/)

本项目是一个面向 Python 初学者的 API 开发入门教学项目，通过三个循序渐进的演示示例，系统教授复杂 Python API 的开发流程与最佳实践。

## 📚 学习目标

通过本项目，你将学习到：

- ✅ Flask 框架的基础和高级用法
- ✅ RESTful API 设计原则
- ✅ 数据库 ORM（SQLAlchemy）使用
- ✅ 数据序列化和验证（Marshmallow）
- ✅ 应用架构设计（应用工厂、蓝图）
- ✅ 数据库迁移管理
- ✅ 错误处理和日志配置
- ✅ 单元测试和集成测试
- ✅ 使用 UV 进行 Python 项目管理

## 🏗️ 项目结构

```
demo-uv-python/
├── demo1/                 # 基础示例：内存存储
│   ├── app.py
│   ├── tests/
│   └── README.md
├── demo2/                 # 进阶示例：数据库持久化
│   ├── app.py
│   ├── tests/
│   └── README.md
├── demo3/                 # 生产示例：模块化架构
│   ├── app/
│   ├── tests/
│   ├── migrations/
│   └── README.md
├── scripts/               # 工具脚本
├── pyproject.toml        # UV 项目配置
├── AGENTS.md            # 开发规范和工具选型说明
└── README.md            # 本文档
```

## 🚀 快速开始

### 环境要求

- Python >= 3.13
- [UV](https://docs.astral.sh/uv/) - 现代 Python 包管理器

> **为什么选择 UV？**
> - ⚡ 极速：使用 Rust 编写，比 pip 快 10-100 倍
> - 📦 一体化：替代 pip、venv、pip-tools、virtualenv 等工具
> - 🔒 锁定文件：自动生成 `uv.lock` 确保环境一致
> - 🚀 原生支持：无需额外工具即可运行脚本

### 安装依赖

```bash
# 克隆项目后，安装所有依赖
uv sync

# 安装开发依赖（包含测试工具）
uv sync --group dev
```

## 🛠️ 常用命令

本项目采用**原生 UV 命令**运行，无需额外配置。所有命令都通过 `uv run` 直接执行。

### 运行示例

```bash
# 运行 Demo1（基础 API）
uv run demo1/app.py

# 运行 Demo2（数据库版）
cd demo2 && uv run app.py

# 运行 Demo3（生产级）
cd demo3 && uv run run.py
```

### 测试

```bash
# 分别运行各示例测试（推荐，避免模块名冲突）
uv run pytest demo1/tests -v
uv run pytest demo2/tests -v
uv run pytest demo3/tests -v

# 或使用分号顺序执行
uv run pytest demo1/tests -v && uv run pytest demo2/tests -v && uv run pytest demo3/tests -v
```

### 代码质量

```bash
# 格式化代码
uv run black demo1/ demo2/ demo3/ --line-length 88

# 语法检查
uv run python -m py_compile demo1/app.py demo2/app.py demo3/run.py

# 清理缓存文件
find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
```

### 数据库操作（Demo3）

```bash
# 初始化迁移（首次）
cd demo3 && uv run flask --app "app:create_app('develop')" db init

# 生成迁移脚本
cd demo3 && uv run flask --app "app:create_app('develop')" db migrate -m "描述信息"

# 应用迁移
cd demo3 && uv run flask --app "app:create_app('develop')" db upgrade
```

### 其他工具

```bash
# 生成测试数据
uv run scripts/batch-insert.py --users 10 --posts 5
```

## 📖 三个演示示例

### Demo1: 基础 Flask API

**特点**：
- 单文件应用结构
- 内存数据存储
- 基础 CRUD 操作
- 简单错误处理

**适合学习**：Flask 基础、路由定义、请求处理

```bash
uv run demo1/app.py
```

[查看详情 →](demo1/README.md)

### Demo2: 数据库版 API

**特点**：
- SQLite 数据持久化
- SQLAlchemy ORM
- 一对多关联关系
- 分页查询和筛选
- 结构化错误响应

**适合学习**：数据库操作、ORM 使用、查询优化

```bash
cd demo2 && uv run app.py
```

[查看详情 →](demo2/README.md)

### Demo3: 生产级模块化 API

**特点**：
- 应用工厂模式
- 蓝图组织路由
- 数据库迁移（Alembic）
- Marshmallow 数据验证
- 统一响应格式
- 完整错误处理
- 日志配置
- 全面测试覆盖

**适合学习**：大型项目架构、生产最佳实践

```bash
cd demo3 && uv run run.py
```

[查看详情 →](demo3/README.md)

## 📊 示例演进对比

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
| 测试覆盖 | ✅ | ✅ | ✅ |
| 生产就绪 | ❌ | ❌ | ✅ |

## 🧪 测试详情

```bash
# 分别运行各示例测试并生成覆盖率报告
uv run pytest demo1/tests --cov=demo1 --cov-report=html
uv run pytest demo2/tests --cov=demo2 --cov-report=html
uv run pytest demo3/tests --cov=app --cov-report=html

# 查看 HTML 报告
open htmlcov/index.html  # macOS
```

## 📡 API 使用示例

启动任意 Demo 后，可以使用以下命令测试 API：

```bash
# 健康检查
curl http://127.0.0.1:3000/health

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
```

## ⚙️ 配置说明

### 环境变量

```bash
# 配置环境（develop/test/product）
export FLASK_CONFIG=develop

# 数据库 URL（生产环境）
export DATABASE_URL=postgresql://user:pass@localhost/dbname

# 密钥（生产环境必需）
export SECRET_KEY=your-secret-key
```

### 代码风格

本项目使用 [Black](https://github.com/psf/black) 进行代码格式化：

```bash
# 格式化代码
uv run black demo1/ demo2/ demo3/ --line-length 88
```

## 📚 学习路径建议

### 初学者路径

1. **Demo1**：理解 Flask 基础概念
   - 路由定义
   - 请求处理
   - JSON 响应

2. **Demo2**：学习数据库操作
   - SQLAlchemy ORM
   - 数据模型定义
   - 关联关系

3. **Demo3**：掌握生产级架构
   - 应用工厂
   - 蓝图组织
   - 数据库迁移

### 进阶学习

- 阅读 [AGENTS.md](AGENTS.md) 了解开发规范和工具选型
- 查看测试文件学习测试编写
- 研究错误处理和日志配置

## 🎯 工具选型说明

### 为什么选择原生 UV 命令？

本项目直接使用 `uv run` 命令运行，**不引入 Makefile、Taskipy 或 Poe** 等额外工具。

#### 方案对比

| 方案 | 优点 | 缺点 | 选择 |
|------|------|------|------|
| **Makefile** | 通用、历史悠久 | 语法古老、Windows 需额外安装 | ❌ |
| **Taskipy** | 轻量、集成 pyproject.toml | 额外依赖 | ❌ |
| **Poe the Poet** | 功能丰富、任务依赖 | 额外依赖、配置复杂 | ❌ |
| **原生 UV** | 零额外依赖、简单直接 | 命令稍长 | ✅ |

#### 选择理由

1. **教学友好**
   - 初学者只需学习 UV 一个工具
   - 无需理解 Makefile 的 Tab 缩进规则
   - 无需学习 Taskipy/Poe 的配置语法

2. **依赖最小化**
   - 零额外依赖（仅需 UV）
   - 避免工具链过于复杂
   - 降低环境配置门槛

3. **透明直接**
   - 命令直接可见，无封装黑盒
   - 便于理解每个命令的具体作用
   - 调试更方便

4. **未来可迁移**
   - 当项目复杂化时，可随时引入 Taskipy/Poe
   - 迁移成本极低（只是命令别名）

#### 何时应该引入 Taskipy/Poe？

当项目出现以下情况时，建议迁移到 Taskipy：

- 命令数量超过 10 个，记忆困难
- 存在复杂的命令依赖链（如 `test` 依赖 `lint`）
- 需要频繁切换不同参数运行同一命令
- 团队成员对 Makefile 不熟悉且环境不统一

**迁移示例**（当前原生 UV → 未来 Taskipy）：

```bash
# 当前：原生 UV
uv run pytest demo1/tests -v

# 未来：Taskipy
uv run task test-demo1
```

只需在 `pyproject.toml` 添加配置，命令本身无需修改。

## 🔗 相关资源

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Marshmallow](https://marshmallow.readthedocs.io/)
- [UV 文档](https://docs.astral.sh/uv/)

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

> 💡 **提示**：每个 Demo 目录下都有详细的 README.md 文档，包含该示例的详细说明和使用方法。
