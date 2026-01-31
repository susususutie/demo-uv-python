# app/views/post.py
from flask import Blueprint, request, jsonify, abort
from app.extensions import db
from app.models import Post, User
from app.schemas import post_schema, posts_schema
from app.utils import apply_filter, apply_sort, get_page_params, to_pagination_dict

bp = Blueprint("post", __name__, url_prefix="/api/posts")


# 获取所有文章
@bp.get("")
def list_posts():
    query = db.session.query(Post)
    p = request.args.to_dict()

    query = apply_filter(
        query,
        Post,
        allowed_cols={
            "keyword": ("title,content", "contains"),
            "title": ("title", "contains"),
            "description": ("description", "contains"),
        },
        params=p,
    )
    query = apply_sort(
        query,
        Post,
        allowed_cols={"title", "created_at", "updated_at"},
        default_col="updated_at",
        default_dir="desc",
        params=p,
    )
    pager = get_page_params(params=p)

    pagination = query.paginate(error_out=False, **pager)

    return jsonify(
        {
            "list": posts_schema.dump(pagination.items, many=True),
            "pagination": to_pagination_dict(pagination),
        }
    )


# 创建文章
@bp.post("")
def create_post():
    data = post_schema.load(request.json)  # 校验

    # 可选：验证 user 存在
    db.session.get(User, data["user_id"]) or abort(404)

    post = Post(**data)
    db.session.add(post)
    db.session.commit()
    return jsonify(post_schema.dump(post)), 201


# 获取单篇文章
@bp.get("/<int:pid>")
def get_post(pid):
    post = db.session.get(Post, pid) or abort(404)
    return jsonify(post_schema.dump(post))


# 更新文章
@bp.put("/<int:pid>")
def update_post(pid):
    post = db.session.get(Post, pid) or abort(404)
    data = post_schema.load(request.json, partial=True)
    for key, value in data.items():
        setattr(post, key, value)
    db.session.commit()
    return jsonify(post_schema.dump(post))


# 删除文章
@bp.delete("/<int:pid>")
def delete_post(pid):
    post = db.session.get(Post, pid) or abort(404)
    db.session.delete(post)
    db.session.commit()
    return "", 204
