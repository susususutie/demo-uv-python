"""Demo3 文章管理视图模块。

提供文章相关的 CRUD 接口。
"""

from flask import Blueprint, request

from app.extensions import db
from app.models import Post, User
from app.schemas import post_schema, posts_schema
from app.utils import apply_filter, apply_sort, get_page_params, to_pagination_dict
from app.responses import success, created, no_content
from app.errors import NotFoundError

bp = Blueprint("post", __name__, url_prefix="/api/posts")


@bp.get("")
def list_posts():
    """获取文章列表。

    查询参数:
        page: 页码，默认 1
        per_page: 每页条数，默认 10，最大 100
        keyword: 搜索关键词（匹配标题或内容）
        title: 按标题筛选
        published: 是否只显示已发布（true/false）
        sort: 排序字段（title, created_at, updated_at）
        order: 排序方向（asc, desc）

    Returns:
        文章列表和分页信息
    """
    query = db.session.query(Post)
    params = request.args.to_dict()

    # 应用过滤条件
    query = apply_filter(
        query,
        Post,
        allowed_cols={
            "keyword": ("title,content", "contains"),
            "title": ("title", "contains"),
        },
        params=params,
    )

    # 按发布状态筛选
    published = params.get("published")
    if published is not None:
        is_published = published.lower() == "true"
        query = query.filter_by(published=is_published)

    # 应用排序
    query = apply_sort(
        query,
        Post,
        allowed_cols={"title", "created_at", "updated_at"},
        default_col="updated_at",
        default_dir="desc",
        params=params,
    )

    # 分页
    pager = get_page_params(params=params)
    pagination = query.paginate(error_out=False, **pager)

    return success(
        {
            "list": posts_schema.dump(pagination.items),
            "pagination": to_pagination_dict(pagination),
        }
    )


@bp.post("")
def create_post():
    """创建新文章。

    请求体:
        {
            "title": "文章标题（必填）",
            "content": "文章内容",
            "user_id": 1,  // 作者 ID（必填）
            "published": false  // 是否发布（可选，默认 false）
        }

    Returns:
        201: 创建成功
    """
    data = post_schema.load(request.json)

    # 验证用户存在
    user = db.session.get(User, data["user_id"])
    if not user:
        raise NotFoundError("用户")

    try:
        post = Post(**data)
        db.session.add(post)
        db.session.commit()
        return created(post_schema.dump(post))
    except Exception as e:
        db.session.rollback()
        raise


@bp.get("/<int:pid>")
def get_post(pid: int):
    """获取文章详情。

    Args:
        pid: 文章 ID
    """
    post = db.session.get(Post, pid)
    if not post:
        raise NotFoundError("文章")
    return success(post_schema.dump(post))


@bp.put("/<int:pid>")
def update_post(pid: int):
    """更新文章。

    Args:
        pid: 文章 ID

    请求体:
        {
            "title": "新标题（可选）",
            "content": "新内容（可选）",
            "published": true  // 可选
        }
    """
    post = db.session.get(Post, pid)
    if not post:
        raise NotFoundError("文章")

    data = post_schema.load(request.json, partial=True)
    for key, value in data.items():
        setattr(post, key, value)

    try:
        db.session.commit()
        return success(post_schema.dump(post), message="文章更新成功")
    except Exception as e:
        db.session.rollback()
        raise


@bp.delete("/<int:pid>")
def delete_post(pid: int):
    """删除文章。

    Args:
        pid: 文章 ID
    """
    post = db.session.get(Post, pid)
    if not post:
        raise NotFoundError("文章")

    try:
        db.session.delete(post)
        db.session.commit()
        return no_content()
    except Exception as e:
        db.session.rollback()
        raise
