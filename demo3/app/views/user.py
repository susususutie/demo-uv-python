# app/views/user.py
from flask import Blueprint, request, jsonify
from app.models import User, db
from app.schemas import user_schema
from app.utils import apply_filter, apply_sort, get_page_params, to_pagination_dict

bp = Blueprint("user", __name__, url_prefix="/api/users")


@bp.get("")
def list_users():
    query = User.query
    p = request.args.to_dict()

    query = apply_filter(
        query,
        User,
        allowed_cols={
            # "id": ("id", "exact"),
            "keyword": ("username,email", "contains"),
            "username": ("username", "contains"),
            "email": ("email", "contains"),
            # "age_min": ("age", "gte"),
        },
        params=p,
    )
    query = apply_sort(
        query,
        User,
        allowed_cols={"username", "email", "created_at"},
        default_col="created_at",
        default_dir="desc",
        params=p,
    )
    pager = get_page_params(params=p)

    pagination = query.paginate(error_out=False, **pager)

    return jsonify(
        {
            "list": user_schema.dump(pagination.items, many=True),
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
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user))


@bp.put("/<int:id>")
def update_user(id):
    user = User.query.get_or_404(id)
    data = user_schema.load(request.json)
    user.username = data["username"]
    user.email = data["email"]
    db.session.commit()
    return jsonify(user_schema.dump(user))


@bp.delete("/<int:id>")
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user_schema.dump(user))
