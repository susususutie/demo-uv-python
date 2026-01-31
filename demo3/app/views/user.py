# app/views/user.py
from flask import Blueprint, request, jsonify, abort
from sqlalchemy import func
from app.models import User, Post, db
from app.schemas import user_schema
from app.utils import apply_filter, apply_sort, get_page_params, to_pagination_dict

bp = Blueprint("user", __name__, url_prefix="/api/users")


@bp.get("")
def list_users():
    # 查询用户并统计文章数量
    query = db.session.query(
        User,
        func.count(Post.id).label('article_count')
    ).outerjoin(
        Post, User.id == Post.user_id
    ).group_by(User.id)
    
    p = request.args.to_dict()

    # 由于查询结构变化，手动处理过滤和排序
    if p.get('keyword'):
        query = query.filter(
            db.or_(
                User.username.contains(p['keyword']),
                User.email.contains(p['keyword'])
            )
        )
    if p.get('username'):
        query = query.filter(User.username.contains(p['username']))
    if p.get('email'):
        query = query.filter(User.email.contains(p['email']))
    
    # 排序
    sort_col = p.get('sort', 'created_at')
    sort_dir = p.get('order', 'desc')
    if sort_col in ['username', 'email', 'created_at']:
        sort_field = getattr(User, sort_col)
        if sort_dir == 'desc':
            sort_field = sort_field.desc()
        query = query.order_by(sort_field)
    
    pager = get_page_params(params=p)
    pagination = query.paginate(error_out=False, **pager)

    # 构建返回数据，包含文章数量
    user_list = []
    for user, article_count in pagination.items:
        user_data = user_schema.dump(user)
        user_data['article_count'] = article_count or 0
        user_list.append(user_data)

    return jsonify(
        {
            "list": user_list,
            "pagination": to_pagination_dict(pagination),
        }
    )


@bp.post("")
def create_user():
    # 1. schemas 反序列化+校验
    data = user_schema.load(request.json)

    # 2. models 写入
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    # 3. schemas 序列化返回
    return jsonify(user_schema.dump(user)), 201


@bp.get("/<int:id>")
def get_user(id):
    # 查询用户并统计文章数量
    result = db.session.query(
        User,
        func.count(Post.id).label('article_count')
    ).outerjoin(
        Post, User.id == Post.user_id
    ).filter(
        User.id == id
    ).group_by(User.id).first()
    
    if not result:
        return jsonify({"error": "User not found"}), 404
    
    user, article_count = result
    user_data = user_schema.dump(user)
    user_data['article_count'] = article_count or 0
    
    return jsonify(user_data)


@bp.put("/<int:id>")
def update_user(id):
    user = db.session.get(User, id) or abort(404)
    data = user_schema.load(request.json)
    user.username = data["username"]
    user.email = data["email"]
    db.session.commit()
    return jsonify(user_schema.dump(user))


@bp.delete("/<int:id>")
def delete_user(id):
    user = db.session.get(User, id) or abort(404)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))
