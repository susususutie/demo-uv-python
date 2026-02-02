"""
Demo2: 数据库版 Flask API 示例

本模块演示使用 Flask-SQLAlchemy 实现持久化存储的 REST API。
在 Demo1 的基础上增加了：
    - 数据库持久化（SQLite）
    - 数据模型定义
    - 关联关系（一对多）
    - 分页查询
    - 更完善的错误处理

数据模型：
    - User: 用户表
    - Post: 文章表（与用户一对多关联）

运行方式：
    cd demo2 && uv run app.py

访问地址：
    http://127.0.0.1:3000
"""

import os
from datetime import datetime, timezone
from typing import Any, Optional

from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

# =============================================================================
# 应用配置
# =============================================================================

app = Flask(__name__)

# 数据库配置
# 使用绝对路径确保数据库文件位置正确
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'instance', 'api.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# JSON 配置：支持中文显示，保持字段顺序
app.json.ensure_ascii = False
app.config["JSON_SORT_KEYS"] = False

# 初始化数据库
db = SQLAlchemy(app)


# =============================================================================
# 数据模型
# =============================================================================


class User(db.Model):
    """用户模型。

    属性:
        id: 主键，自增整数
        username: 用户名，唯一，非空
        email: 邮箱地址，唯一，非空
        created_at: 创建时间
        posts: 关联的文章列表（一对多）
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # 一对多关系：一个用户可以有多篇文章
    # cascade="all, delete-orphan" 表示删除用户时同时删除关联文章
    posts = db.relationship(
        "Post", backref="author", lazy="dynamic", cascade="all, delete-orphan"
    )

    def to_dict(self) -> dict[str, Any]:
        """将模型实例转换为字典。

        Returns:
            包含用户数据的字典
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "post_count": self.posts.count(),
        }


class Post(db.Model):
    """文章模型。

    属性:
        id: 主键，自增整数
        title: 文章标题，非空
        content: 文章内容，非空
        published: 是否发布
        created_at: 创建时间
        updated_at: 最后更新时间
        user_id: 外键，关联用户 ID
    """

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def to_dict(self) -> dict[str, Any]:
        """将模型实例转换为字典。

        Returns:
            包含文章数据的字典
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "published": self.published,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
        }


# =============================================================================
# 错误处理
# =============================================================================


@app.errorhandler(404)
def not_found(error) -> Response:
    """处理 404 资源不存在错误。"""
    return (
        jsonify(
            {"error": {"code": "RESOURCE_NOT_FOUND", "message": "请求的资源不存在"}}
        ),
        404,
    )


@app.errorhandler(400)
def bad_request(error) -> Response:
    """处理 400 请求参数错误。"""
    return jsonify({"error": {"code": "BAD_REQUEST", "message": "请求参数无效"}}), 400


@app.errorhandler(500)
def internal_error(error) -> Response:
    """处理 500 服务器内部错误。"""
    db.session.rollback()  # 回滚数据库事务
    return (
        jsonify({"error": {"code": "INTERNAL_ERROR", "message": "服务器内部错误"}}),
        500,
    )


# =============================================================================
# 辅助函数
# =============================================================================


def get_pagination_params(
    max_per_page: int = 100, default_per_page: int = 10
) -> tuple[int, int]:
    """从请求参数中获取分页信息。

    Args:
        max_per_page: 每页最大条数限制
        default_per_page: 默认每页条数

    Returns:
        (page, per_page) 元组
    """
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", default_per_page, type=int)
    except (ValueError, TypeError):
        page = 1
        per_page = default_per_page

    # 范围校验
    page = max(1, page)
    per_page = max(1, min(per_page, max_per_page))

    return page, per_page


def make_pagination_response(pagination) -> dict[str, Any]:
    """构建分页响应数据。

    Args:
        pagination: SQLAlchemy 分页对象

    Returns:
        分页元信息字典
    """
    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "has_prev": pagination.has_prev,
        "has_next": pagination.has_next,
    }


# =============================================================================
# 路由 - 首页和健康检查
# =============================================================================


@app.route("/")
def api_info() -> Response:
    """API 信息首页。"""
    return jsonify(
        {
            "message": "Flask API Server",
            "version": "2.0",
            "demo": "数据库持久化版 API",
            "endpoints": {
                "users": "/api/users",
                "posts": "/api/posts",
                "health": "/health",
            },
        }
    )


@app.route("/health")
def health_check() -> Response:
    """健康检查端点，用于监控服务状态。"""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "database": "connected",
        }
    )


# =============================================================================
# 路由 - 用户管理
# =============================================================================


@app.route("/api/users", methods=["GET"])
def get_users() -> Response:
    """获取用户列表（支持分页）。

    查询参数:
        page: 页码，默认 1
        per_page: 每页条数，默认 10，最大 100

    Returns:
        用户列表和分页信息
    """
    page, per_page = get_pagination_params()

    # 构建查询
    query = User.query

    # 可选：关键词搜索
    keyword = request.args.get("keyword")
    if keyword:
        query = query.filter(
            or_(User.username.contains(keyword), User.email.contains(keyword))
        )

    # 执行分页查询
    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "list": [user.to_dict() for user in pagination.items],
            "pagination": make_pagination_response(pagination),
        }
    )


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Response:
    """获取单个用户详情。

    Args:
        user_id: 用户 ID

    Returns:
        用户详情数据
    """
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@app.route("/api/users", methods=["POST"])
def create_user() -> Response:
    """创建新用户。

    请求体:
        {
            "username": "用户名",
            "email": "邮箱地址"
        }

    Returns:
        201: 创建成功
        400: 参数错误或重复
    """
    data: Optional[dict[str, Any]] = request.get_json()

    if not data:
        return (
            jsonify({"error": {"code": "EMPTY_BODY", "message": "请求体不能为空"}}),
            400,
        )

    if "username" not in data or "email" not in data:
        return (
            jsonify(
                {
                    "error": {
                        "code": "MISSING_FIELDS",
                        "message": "缺少必要字段: username 和 email",
                    }
                }
            ),
            400,
        )

    # 检查唯一性
    if User.query.filter_by(username=data["username"]).first():
        return (
            jsonify(
                {"error": {"code": "DUPLICATE_USERNAME", "message": "用户名已存在"}}
            ),
            400,
        )

    if User.query.filter_by(email=data["email"]).first():
        return (
            jsonify({"error": {"code": "DUPLICATE_EMAIL", "message": "邮箱已被使用"}}),
            400,
        )

    # 创建用户
    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id: int) -> Response:
    """更新用户信息。

    Args:
        user_id: 要更新的用户 ID

    请求体:
        {
            "username": "新用户名（可选）",
            "email": "新邮箱（可选）"
        }
    """
    user = User.query.get_or_404(user_id)
    data: Optional[dict[str, Any]] = request.get_json()

    if not data:
        return (
            jsonify({"error": {"code": "EMPTY_BODY", "message": "请求体不能为空"}}),
            400,
        )

    # 更新用户名
    if "username" in data:
        existing = User.query.filter_by(username=data["username"]).first()
        if existing and existing.id != user_id:
            return (
                jsonify(
                    {"error": {"code": "DUPLICATE_USERNAME", "message": "用户名已存在"}}
                ),
                400,
            )
        user.username = data["username"]

    # 更新邮箱
    if "email" in data:
        existing = User.query.filter_by(email=data["email"]).first()
        if existing and existing.id != user_id:
            return (
                jsonify(
                    {"error": {"code": "DUPLICATE_EMAIL", "message": "邮箱已被使用"}}
                ),
                400,
            )
        user.email = data["email"]

    db.session.commit()
    return jsonify(user.to_dict())


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int) -> Response:
    """删除用户。

    Args:
        user_id: 要删除的用户 ID

    Note:
        删除用户会级联删除其所有文章
    """
    user = User.query.get_or_404(user_id)

    # 检查是否有文章（虽然设置了级联删除，但这里可以做额外检查）
    post_count = user.posts.count()

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "用户删除成功", "deleted_posts": post_count})


# =============================================================================
# 路由 - 文章管理
# =============================================================================


@app.route("/api/posts", methods=["GET"])
def get_posts() -> Response:
    """获取文章列表（支持分页和筛选）。

    查询参数:
        page: 页码，默认 1
        per_page: 每页条数，默认 10
        user_id: 按作者筛选（可选）
        published: 只显示已发布的（可选，true/false）
        keyword: 标题或内容关键词搜索（可选）
    """
    page, per_page = get_pagination_params()

    # 构建查询
    query = Post.query

    # 筛选条件
    user_id = request.args.get("user_id", type=int)
    if user_id:
        query = query.filter_by(user_id=user_id)

    published_only = request.args.get("published", "").lower() == "true"
    if published_only:
        query = query.filter_by(published=True)

    keyword = request.args.get("keyword")
    if keyword:
        query = query.filter(
            or_(Post.title.contains(keyword), Post.content.contains(keyword))
        )

    # 排序：最新的在前
    pagination = query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "list": [post.to_dict() for post in pagination.items],
            "pagination": make_pagination_response(pagination),
        }
    )


@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id: int) -> Response:
    """获取单篇文章详情。"""
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@app.route("/api/posts", methods=["POST"])
def create_post() -> Response:
    """创建新文章。

    请求体:
        {
            "title": "文章标题",
            "content": "文章内容",
            "user_id": 1,
            "published": false  // 可选，默认 false
        }
    """
    data: Optional[dict[str, Any]] = request.get_json()

    if not data:
        return (
            jsonify({"error": {"code": "EMPTY_BODY", "message": "请求体不能为空"}}),
            400,
        )

    required = ["title", "content", "user_id"]
    missing = [f for f in required if f not in data]
    if missing:
        return (
            jsonify(
                {
                    "error": {
                        "code": "MISSING_FIELDS",
                        "message": f"缺少必要字段: {', '.join(missing)}",
                    }
                }
            ),
            400,
        )

    # 验证用户存在
    user = User.query.get(data["user_id"])
    if not user:
        return (
            jsonify(
                {"error": {"code": "USER_NOT_FOUND", "message": "指定的用户不存在"}}
            ),
            400,
        )

    post = Post(
        title=data["title"],
        content=data["content"],
        user_id=data["user_id"],
        published=data.get("published", False),
    )
    db.session.add(post)
    db.session.commit()

    return jsonify(post.to_dict()), 201


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id: int) -> Response:
    """更新文章信息。"""
    post = Post.query.get_or_404(post_id)
    data: Optional[dict[str, Any]] = request.get_json()

    if not data:
        return (
            jsonify({"error": {"code": "EMPTY_BODY", "message": "请求体不能为空"}}),
            400,
        )

    if "title" in data:
        post.title = data["title"]
    if "content" in data:
        post.content = data["content"]
    if "published" in data:
        post.published = data["published"]

    db.session.commit()
    return jsonify(post.to_dict())


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id: int) -> Response:
    """删除文章。"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return "", 204


# =============================================================================
# 应用入口
# =============================================================================

if __name__ == "__main__":
    # 确保实例目录存在
    os.makedirs("instance", exist_ok=True)

    # 创建所有数据库表
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=3000, debug=True)
