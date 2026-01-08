# app/views/post.py
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Post, User
from app.schemas import post_schema, posts_schema

bp = Blueprint("post", __name__, url_prefix="/api/posts")


# 获取所有文章
@bp.get("")
def list_posts():
    posts = Post.query.all()
    return jsonify(posts_schema.dump(posts))


# 创建文章
@bp.post("")
def create_post():
    data = post_schema.load(request.json)  # 校验

    # 可选：验证 user 存在
    User.query.get_or_404(data["user_id"])

    post = Post(**data)
    db.session.add(post)
    db.session.commit()
    return jsonify(post_schema.dump(post)), 201


# 获取单篇文章
@bp.get("/<int:pid>")
def get_post(pid):
    post = Post.query.get_or_404(pid)
    return jsonify(post_schema.dump(post))


# 更新文章
@bp.put("/<int:pid>")
def update_post(pid):
    post = Post.query.get_or_404(pid)
    data = post_schema.load(request.json, partial=True)
    for key, value in data.items():
        setattr(post, key, value)
    db.session.commit()
    return jsonify(post_schema.dump(post))


# 删除文章
@bp.delete("/<int:pid>")
def delete_post(pid):
    post = Post.query.get_or_404(pid)
    db.session.delete(post)
    db.session.commit()
    return "", 204
