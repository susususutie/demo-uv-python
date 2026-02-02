# Demo2: 数据库版 Flask API

本示例演示使用 Flask-SQLAlchemy 实现持久化存储的 REST API，在 Demo1 的基础上增加了数据库支持。

## 学习目标

- 理解 Flask-SQLAlchemy 的基本使用
- 掌握数据模型定义和关系映射
- 学习数据库查询和分页
- 了解关联关系（一对多）的实现

## 新增特性

- **持久化存储**：使用 SQLite 数据库存储数据
- **数据模型**：使用 SQLAlchemy ORM 定义模型
- **关联关系**：用户与文章的一对多关系
- **分页查询**：支持分页和筛选的列表接口
- **完善的错误处理**：结构化错误响应

## 项目结构

```
demo2/
├── app.py              # 主应用文件（单文件，但结构清晰）
├── tests/              # 测试目录
│   ├── __init__.py
│   ├── conftest.py     # 测试配置
│   ├── test_health.py  # 健康检查测试
│   ├── test_users.py   # 用户 API 测试
│   └── test_posts.py   # 文章 API 测试
├── instance/           # 数据库文件目录（运行时创建）
└── README.md           # 说明文档
```

## 数据模型

### User（用户）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| username | String(80) | 用户名，唯一 |
| email | String(120) | 邮箱，唯一 |
| created_at | DateTime | 创建时间 |
| posts | Relationship | 关联的文章列表 |

### Post（文章）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键，自增 |
| title | String(200) | 标题 |
| content | Text | 内容 |
| published | Boolean | 是否发布 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |
| user_id | ForeignKey | 作者 ID |

## 运行应用

```bash
cd demo2 && uv run app.py
```

数据库文件将自动在 `instance/` 目录下创建。

## API 端点

### 系统端点

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | API 信息 |
| GET | `/health` | 健康检查 |

### 用户管理

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/users` | 用户列表（支持分页、搜索） |
| GET | `/api/users/<id>` | 用户详情 |
| POST | `/api/users` | 创建用户 |
| PUT | `/api/users/<id>` | 更新用户 |
| DELETE | `/api/users/<id>` | 删除用户 |

#### 用户列表查询参数

- `page`: 页码（默认 1）
- `per_page`: 每页条数（默认 10，最大 100）
- `keyword`: 搜索关键词（匹配用户名或邮箱）

### 文章管理

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/posts` | 文章列表（支持筛选） |
| GET | `/api/posts/<id>` | 文章详情 |
| POST | `/api/posts` | 创建文章 |
| PUT | `/api/posts/<id>` | 更新文章 |
| DELETE | `/api/posts/<id>` | 删除文章 |

#### 文章列表查询参数

- `page`, `per_page`: 分页参数
- `user_id`: 按作者筛选
- `published`: 只显示已发布（`true`）
- `keyword`: 关键词搜索（标题或内容）

## 测试

```bash
uv run pytest demo2/tests -v
```

## 示例请求

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

## 错误响应格式

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "人类可读的错误描述"
    }
}
```

常见错误码：

| 错误码 | 说明 |
|--------|------|
| RESOURCE_NOT_FOUND | 资源不存在 |
| BAD_REQUEST | 请求参数无效 |
| MISSING_FIELDS | 缺少必填字段 |
| DUPLICATE_USERNAME | 用户名已存在 |
| DUPLICATE_EMAIL | 邮箱已被使用 |
| USER_NOT_FOUND | 用户不存在 |

## 批量生成数据

```bash
uv run scripts/batch-insert.py --users 20 --posts 100
```

## 与 Demo1 的区别

| 特性 | Demo1 | Demo2 |
|------|-------|-------|
| 存储方式 | 内存 | SQLite 数据库 |
| 数据持久化 | ❌ | ✅ |
| 数据模型 | 字典 | SQLAlchemy ORM |
| 关联关系 | ❌ | ✅ |
| 分页查询 | ❌ | ✅ |
| 数据筛选 | ❌ | ✅ |
| 错误码 | 简单 | 结构化 |

## 下一步

学习 [Demo3](../demo3/README.md) - 生产级模块化架构。
