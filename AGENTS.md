# Demo UV Python - Agent Guide

## 项目概述

这是一个面向Python初学者的API开发入门教学项目，通过三个循序渐进的Demo演示Flask API开发的最佳实践：

- **demo1**: 基础Flask API（内存存储）
- **demo2**: 数据库版API（单文件，SQLAlchemy）
- **demo3**: 生产级模块化API（应用工厂、蓝图、迁移）

## 项目结构

```
demo-uv-python/
├── demo1/              # 基础示例
│   ├── app.py          # 主应用文件
│   ├── README.md       # Demo1 说明文档
│   └── tests/          # 测试文件
├── demo2/              # 数据库示例
│   ├── app.py          # 主应用文件
│   ├── README.md       # Demo2 说明文档
│   ├── tests/          # 测试文件
│   └── instance/       # 数据库文件目录
├── demo3/              # 生产级示例
│   ├── app/            # 应用包
│   │   ├── __init__.py
│   │   ├── models.py   # 数据模型
│   │   ├── schemas.py  # 序列化模式
│   │   ├── utils.py    # 工具函数
│   │   ├── errors.py   # 错误处理（新增）
│   │   ├── responses.py # 响应工具（新增）
│   │   ├── extensions.py # 扩展实例
│   │   └── views/      # 视图/路由
│   ├── config.py       # 配置文件
│   ├── run.py          # 启动脚本
│   ├── tests/          # 测试文件
│   └── migrations/     # 数据库迁移
├── scripts/            # 工具脚本
├── pyproject.toml     # UV 项目配置
└── README.md          # 主文档
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

### 代码风格

- **格式化**：Black（行长度 88）
- **类型注解**：Python 3.9+ 内置类型（`list[str]` 而非 `List[str]`）
- **文档字符串**：Google Style

### 依赖管理

生产依赖：
```toml
dependencies = [
    "flask>=3.1.2",
    "flask-sqlalchemy>=3.1.1",
    # ...
]
```

开发依赖：
```toml
[dependency-groups]
dev = [
    "pytest>=9.0.2",
    "pytest-flask>=1.3.0",
    # ...
]
```

## 代码规范

### Python 风格

- 遵循 PEP 8 规范
- 使用 Black 进行代码格式化（行长度 88）
- 使用类型注解
- 编写完整的文档字符串（Google Style）

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
        "pages": 10
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

1. 更新数据模型（如果需要）
2. 更新序列化模式
3. 实现视图函数
4. 添加测试用例
5. 更新文档

### 数据库迁移（demo3）

使用原生 UV 命令：

```bash
# 初始化迁移（首次）
cd demo3 && uv run flask --app "app:create_app('develop')" db init

# 生成迁移脚本
cd demo3 && uv run flask --app "app:create_app('develop')" db migrate -m "描述信息"

# 应用迁移
cd demo3 && uv run flask --app "app:create_app('develop')" db upgrade
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
find . -type f -name '*.pyc' -delete 2>/dev/null || true
```

### 数据库

```bash
# Demo3 数据库迁移
cd demo3 && uv run flask --app "app:create_app('develop')" db init
cd demo3 && uv run flask --app "app:create_app('develop')" db migrate -m "描述"
cd demo3 && uv run flask --app "app:create_app('develop')" db upgrade
```

### 其他

```bash
# 生成测试数据
uv run scripts/batch-insert.py --users 10 --posts 5
```

## 注意事项

1. **渐进式教学**：保持三个demo的递进关系，每个demo在前一个基础上增加新概念
2. **中文支持**：所有JSON响应需要设置 `ensure_ascii=False`
3. **错误处理**：统一错误响应格式，包含错误码和详细信息
4. **测试覆盖**：核心功能必须有测试覆盖
5. **依赖最小化**：面向初学者，避免引入过多工具链
6. **原生 UV**：所有命令使用 `uv run` 直接运行，不引入额外工具
