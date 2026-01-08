from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///api.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 配置JSON编码，支持中文显示
app.json.ensure_ascii = False

db = SQLAlchemy(app)


# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship(
        "Post", backref="author", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
            "post_count": len(self.posts),
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "published": self.published,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "author_id": self.user_id,
        }


# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "资源不存在"}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "请求数据无效"}), 400


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({"error": "服务器内部错误"}), 500


# API路由
@app.route("/")
def api_info():
    return jsonify(
        {
            "message": "Flask API Server",
            "version": "2.0",
            "endpoints": {
                "users": "/api/users",
                "posts": "/api/posts",
                "health": "/health",
            },
        }
    )


@app.route("/health")
def health_check():
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": "connected",
        }
    )


# 用户相关API
@app.route("/api/users", methods=["GET"])
def get_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    if per_page > 100:
        per_page = 100

    users = User.query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "users": [user.to_dict() for user in users.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": users.total,
                "pages": users.pages,
                "has_prev": users.has_prev,
                "has_next": users.has_next,
            },
        }
    )


@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求数据不能为空"}), 400

    if "username" not in data or "email" not in data:
        return jsonify({"error": "缺少必要字段: username 和 email"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "用户名已存在"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "邮箱已被使用"}), 400

    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "请求数据不能为空"}), 400

    if "username" in data:
        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"error": "用户名已存在"}), 400
        user.username = data["username"]

    if "email" in data:
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user and existing_user.id != user_id:
            return jsonify({"error": "邮箱已被使用"}), 400
        user.email = data["email"]

    db.session.commit()
    return jsonify(user.to_dict())


@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    if user.posts:
        return jsonify({"error": "用户下有文章，无法删除"}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "删除成功"}), 200


# 文章相关API
@app.route("/api/posts", methods=["GET"])
def get_posts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    user_id = request.args.get("user_id", type=int)
    published_only = request.args.get("published", "false").lower() == "true"

    app.logger.debug(
        f"user_id:{request.args.get('user_id', type=int)} published_only: {request.args.get('published', 'false')}"
    )

    if per_page > 100:
        per_page = 100

    query = Post.query
    if published_only:
        query = query.filter_by(published=True)
    if user_id:
        query = query.filter_by(user_id=user_id)

    posts = query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "posts": [post.to_dict() for post in posts.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": posts.total,
                "pages": posts.pages,
                "has_prev": posts.has_prev,
                "has_next": posts.has_next,
            },
        }
    )


@app.route("/api/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@app.route("/api/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "请求数据不能为空"}), 400

    if "title" not in data or "content" not in data or "user_id" not in data:
        return jsonify({"error": "缺少必要字段: title, content, user_id"}), 400

    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "用户不存在"}), 400

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
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "请求数据不能为空"}), 400

    if "title" in data:
        post.title = data["title"]
    if "content" in data:
        post.content = data["content"]
    if "published" in data:
        post.published = data["published"]

    db.session.commit()
    return jsonify(post.to_dict())


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return "", 204


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=3000, debug=True)
