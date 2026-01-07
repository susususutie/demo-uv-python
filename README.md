# demo-uv-python

本项目演示了如何使用 UV（一个用 Rust 编写的超快 Python 包管理和项目工具）进行 Python 项目开发。

## 项目概述

这是一个演示项目，包含以下内容：

- UV 基本命令
- 基于 Flask 的示例应用，实现了基本的 CRUD 操作

## UV 基本命令

创建新项目：

```bash
uv init project-name
```

管理依赖：

```bash
uv add pkg          # 添加依赖
uv remove pkg       # 删除依赖
```

同步依赖：

```bash
uv sync             # 安装 uv.lock 文件中的所有依赖
```

运行项目：

```bash
uv run app.py       # 等同于 uv run python app.py
```

## 示例项目 demo1

一个基础的 Flask API 示例，使用内存存储数据，包含基本的 CRUD 操作。

运行：

```bash
uv run demo1/app.py
```

测试：

```bash
# 访问首页
curl http://127.0.0.1:5000/

# 获取所有用户
curl http://127.0.0.1:5000/users

# 获取用户1
curl http://127.0.0.1:5000/users/1

# 创建用户
curl -X POST http://127.0.0.1:5000/users \
    -H "Content-Type: application/json" \
    -d '{"name": "王五", "email": "wangwu@example.com"}'

# 更新用户1
curl -X PUT http://127.0.0.1:5000/users/1 \
    -H "Content-Type: application/json" \
    -d '{"name": "张三更新", "email": "zhangsan@example.com"}'

# 删除用户1
curl -X DELETE http://127.0.0.1:5000/users/1
```

## 示例项目 demo2

引入数据库、数据模型、分页查询和完善的错误处理及格式化工具。

运行：

```bash
cd demo2 && uv run app.py
```

测试：

```bash
# endpoint
curl http://127.0.0.1:5000/

# health
curl http://127.0.0.1:5000/health

# 获取所有用户
curl http://127.0.0.1:5000/api/users

# 获取用户1
curl http://127.0.0.1:5000/api/users/1

# 创建用户
curl -X POST http://127.0.0.1:5000/api/users \
    -H "Content-Type: application/json" \
    -d '{"username": "王五", "email": "wangwu@example.com"}'

# 更新用户1
curl -X PUT http://127.0.0.1:5000/api/users/1 \
    -H "Content-Type: application/json" \
    -d '{"username": "张三更新", "email": "zhangsan@example.com"}'

# 删除用户1
curl -X DELETE http://127.0.0.1:5000/api/users/1


# 获取所有文章
curl http://127.0.0.1:5000/api/posts

# 获取文章
curl http://127.0.0.1:5000/api/posts/1

# 创建文章
curl -X POST http://127.0.0.1:5000/api/posts \
    -H "Content-Type: application/json" \
    -d '{"user_id": 1, "title": "文章标题", "content": "文章内容"}'

# 更新文章
curl -X PUT http://127.0.0.1:5000/api/posts/1 \
    -H "Content-Type: application/json" \
    -d '{"title": "文章标题更新", "content": "文章内容更新", "published": true}'

# 删除文章
curl -X DELETE http://127.0.0.1:5000/api/posts/1
```

## 数据库文件路径说明

运行 `demo2/app.py` 时，数据库文件位置取决于运行方式：

- `uv run demo2/app.py` → 项目根目录创建 `instance/api.db`
- `cd demo2 && uv run app.py` → demo2 目录创建 `instance/api.db`

**原因**：Flask-SQLAlchemy 3.x 将 SQLite 数据库创建在 Flask 实例目录中，实例目录位置取决于工作目录。

**解决方案**：

1. 显式指定实例目录路径
2. 使用绝对路径的数据库 URI
3. 保持一致的运行方式
4. 使用环境变量控制数据库路径
