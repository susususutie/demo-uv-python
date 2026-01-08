# app/views/user.py
from flask import Blueprint, request, jsonify
from app.models import User, db
from app.schemas import user_schema

bp = Blueprint("user", __name__, url_prefix="/api/users")


@bp.get("")
def list_users():
    users = User.query.all()
    return jsonify(user_schema.dump(users, many=True))


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
