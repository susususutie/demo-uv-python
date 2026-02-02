# Demo1: 基础 Flask API

本示例演示最简单的 Flask REST API 实现，使用内存存储数据，适合初学者理解 Flask 的基本概念。

## 学习目标

- 理解 Flask 应用的基本结构
- 掌握路由定义和请求处理
- 学习 JSON 数据的序列化和反序列化
- 了解基础的 RESTful API 设计

## 项目结构

```
demo1/
├── app.py           # 主应用文件（单文件结构）
├── tests/           # 测试目录
│   ├── __init__.py
│   ├── conftest.py  # 测试配置
│   └── test_app.py  # 测试用例
└── README.md        # 说明文档
```

## 核心概念

### 1. Flask 应用实例

```python
from flask import Flask

app = Flask(__name__)
```

### 2. 路由定义

```python
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)
```

### 3. 请求处理

```python
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    # 处理数据...
```

### 4. 响应返回

```python
return jsonify(data), 201  # 成功创建
return jsonify({"error": "..."}), 404  # 资源不存在
```

## 运行应用

```bash
uv run demo1/app.py
```

应用将在 http://127.0.0.1:3000 启动。

## API 端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | API 信息 |
| GET | `/users` | 获取所有用户 |
| GET | `/users/<id>` | 获取单个用户 |
| POST | `/users` | 创建用户 |
| PUT | `/users/<id>` | 更新用户 |
| DELETE | `/users/<id>` | 删除用户 |

## 测试

```bash
uv run pytest demo1/tests -v
```

## 示例请求

```bash
# 查看 API 信息
curl http://127.0.0.1:3000/

# 获取所有用户
curl http://127.0.0.1:3000/users

# 创建用户
curl -X POST http://127.0.0.1:3000/users \
    -H "Content-Type: application/json" \
    -d '{"name": "王五", "email": "wangwu@example.com"}'

# 更新用户
curl -X PUT http://127.0.0.1:3000/users/1 \
    -H "Content-Type: application/json" \
    -d '{"name": "张三更新"}'

# 删除用户
curl -X DELETE http://127.0.0.1:3000/users/1
```

## 注意事项

1. **数据不持久化**：使用内存存储，应用重启后数据丢失
2. **单线程**：适合学习，不适合生产环境
3. **无数据库依赖**：零配置即可运行

## 下一步

学习 [Demo2](../demo2/README.md) - 引入数据库持久化存储。
