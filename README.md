# demo-uv-python

本项目演示了如何使用 UV（一个用 Rust 编写的超快 Python 包管理和项目工具）进行 Python 项目开发。

## 项目概述

这是一个演示项目，包含以下内容：

- UV 基本命令
- demo1: 一个基于 Flask 的示例应用，实现了基本的 CRUD 操作

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

**运行：**

```bash
uv run demo1/app.py
```

**测试示例：**

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
