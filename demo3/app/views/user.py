"""Demo3 用户管理视图模块。

提供用户相关的 CRUD 接口，使用蓝图组织路由。
"""

from flask import Blueprint, request
from sqlalchemy import func

from app.extensions import db
from app.models import User, Post
from app.schemas import user_schema
from app.utils import apply_filter, apply_sort, get_page_params, to_pagination_dict
from app.responses import success, created, deleted
from app.errors import NotFoundError, DuplicateError

# 创建用户蓝图，URL 前缀为 /api/users
bp = Blueprint("user", __name__, url_prefix="/api/users")


@bp.get("")
def list_users():
    """获取用户列表。

    查询参数:
        page: 页码，默认 1
        per_page: 每页条数，默认 10，最大 100
        keyword: 搜索关键词（匹配用户名或邮箱）
        username: 按用户名筛选
        email: 按邮箱筛选
        sort: 排序字段（username, email, created_at）
        order: 排序方向（asc, desc）

    Returns:
        用户列表和分页信息
    """
    # 查询用户并统计文章数量
    query = (
        db.session.query(User, func.count(Post.id).label("article_count"))
        .outerjoin(Post, User.id == Post.user_id)
        .group_by(User.id)
    )

    params = request.args.to_dict()

    # 手动处理过滤（因为使用了 join 查询）
    if params.get("keyword"):
        query = query.filter(
            db.or_(
                User.username.contains(params["keyword"]),
                User.email.contains(params["keyword"]),
            )
        )
    if params.get("username"):
        query = query.filter(User.username.contains(params["username"]))
    if params.get("email"):
        query = query.filter(User.email.contains(params["email"]))

    # 排序处理
    sort_col = params.get("sort", "created_at")
    sort_dir = params.get("order", "desc")
    if sort_col in ["username", "email", "created_at"]:
        sort_field = getattr(User, sort_col)
        if sort_dir == "desc":
            sort_field = sort_field.desc()
        query = query.order_by(sort_field)

    # 分页
    pager = get_page_params(params=params)
    pagination = query.paginate(error_out=False, **pager)

    # 构建返回数据
    user_list = []
    for user, article_count in pagination.items:
        user_data = user_schema.dump(user)
        user_data["article_count"] = article_count or 0
        user_list.append(user_data)

    return success(
        data={"list": user_list, "pagination": to_pagination_dict(pagination)},
        message="获取用户列表成功",
    )


@bp.post("")
def create_user():
    """创建新用户。

    请求体:
        {
            "username": "用户名（必填，2-80字符）",
            "email": "邮箱地址（必填）"
        }

    Returns:
        201: 创建成功，返回新用户信息
        400: 参数验证失败
        409: 用户名或邮箱已存在
    """
    # Schema 反序列化和验证
    data = user_schema.load(request.json)

    # 检查用户名是否已存在
    if User.query.filter_by(username=data["username"]).first():
        raise DuplicateError("用户名")

    # 检查邮箱是否已存在
    if User.query.filter_by(email=data["email"]).first():
        raise DuplicateError("邮箱")

    # 创建用户
    try:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return created(user_schema.dump(user))
    except Exception as e:
        db.session.rollback()
        raise


@bp.get("/<int:id>")
def get_user(id: int):
    """获取单个用户详情。

    Args:
        id: 用户 ID

    Returns:
        用户详情，包含文章数量
    """
    # 查询用户并统计文章数量
    result = (
        db.session.query(User, func.count(Post.id).label("article_count"))
        .outerjoin(Post, User.id == Post.user_id)
        .filter(User.id == id)
        .group_by(User.id)
        .first()
    )

    if not result:
        raise NotFoundError("用户")

    user, article_count = result
    user_data = user_schema.dump(user)
    user_data["article_count"] = article_count or 0

    return success(user_data)


@bp.put("/<int:id>")
def update_user(id: int):
    """更新用户信息。

    Args:
        id: 用户 ID

    请求体:
        {
            "username": "新用户名（可选）",
            "email": "新邮箱（可选）"
        }

    Returns:
        更新后的用户信息
    """
    user = db.session.get(User, id)
    if not user:
        raise NotFoundError("用户")

    data = user_schema.load(request.json, partial=True)

    # 检查用户名唯一性
    if "username" in data and data["username"] != user.username:
        if User.query.filter_by(username=data["username"]).first():
            raise DuplicateError("用户名")
        user.username = data["username"]

    # 检查邮箱唯一性
    if "email" in data and data["email"] != user.email:
        if User.query.filter_by(email=data["email"]).first():
            raise DuplicateError("邮箱")
        user.email = data["email"]

    try:
        db.session.commit()
        return success(user_schema.dump(user), message="用户更新成功")
    except Exception as e:
        db.session.rollback()
        raise


@bp.delete("/<int:id>")
def delete_user(id: int):
    """删除用户。

    Args:
        id: 用户 ID

    Note:
        删除用户会级联删除其所有文章

    Returns:
        删除成功消息
    """
    user = db.session.get(User, id)
    if not user:
        raise NotFoundError("用户")

    # 获取文章数量（用于返回信息）
    post_count = user.get_post_count()

    try:
        db.session.delete(user)
        db.session.commit()
        return deleted(f"用户删除成功，关联的 {post_count} 篇文章也被删除")
    except Exception as e:
        db.session.rollback()
        raise
