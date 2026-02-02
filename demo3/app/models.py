"""Demo3 数据模型模块。

定义应用的核心数据模型：User、Post、Tag。
使用 SQLAlchemy ORM 进行数据库映射。
"""

from datetime import datetime, timezone

from app.extensions import db


class TimestampMixin:
    """时间戳混入类。

    为模型自动添加 created_at 和 updated_at 字段。
    """

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="创建时间",
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="最后更新时间",
    )


class User(db.Model, TimestampMixin):
    """用户模型。

    代表系统中的注册用户，可以创建多篇文章。

    Attributes:
        id: 主键
        username: 用户名（唯一）
        email: 邮箱地址（唯一）
        created_at: 创建时间
        updated_at: 更新时间
        posts: 关联的文章列表（动态查询）
    """

    __tablename__ = "users"
    __table_args__ = {"comment": "用户表"}

    id = db.Column(db.Integer, primary_key=True, comment="用户ID")
    username = db.Column(
        db.String(80), nullable=False, unique=True, index=True, comment="用户名"
    )
    email = db.Column(db.String(120), unique=True, nullable=True, comment="邮箱地址")

    # 一对多关系：一个用户可以有多篇文章
    # lazy="dynamic" 返回 Query 对象，可以进一步筛选
    # cascade="all, delete-orphan" 删除用户时级联删除文章
    posts = db.relationship(
        "Post", backref="author", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """模型的字符串表示。"""
        return f"<User(id={self.id}, username='{self.username}')>"

    def to_dict(self) -> dict:
        """转换为字典格式。

        Returns:
            包含用户基本信息的字典
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def get_post_count(self) -> int:
        """获取用户的文章数量。

        Returns:
            文章数量
        """
        return self.posts.count()


class Tag(db.Model, TimestampMixin):
    """标签模型。

    用于对文章进行分类标记。

    Attributes:
        id: 主键
        name: 标签名称（唯一）
        created_at: 创建时间
        updated_at: 更新时间
    """

    __tablename__ = "tags"
    __table_args__ = {"comment": "标签表"}

    id = db.Column(db.Integer, primary_key=True, comment="标签ID")
    name = db.Column(
        db.String(50), nullable=False, unique=True, index=True, comment="标签名称"
    )

    def __repr__(self) -> str:
        """模型的字符串表示。"""
        return f"<Tag(id={self.id}, name='{self.name}')>"

    def to_dict(self) -> dict:
        """转换为字典格式。

        Returns:
            包含标签基本信息的字典
        """
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Post(db.Model, TimestampMixin):
    """文章模型。

    代表用户发布的文章/博客。

    Attributes:
        id: 主键
        title: 文章标题
        content: 文章内容
        published: 是否已发布
        created_at: 创建时间
        updated_at: 更新时间
        user_id: 作者 ID（外键）
        author: 作者对象（关联）
    """

    __tablename__ = "posts"
    __table_args__ = {"comment": "文章表"}

    id = db.Column(db.Integer, primary_key=True, comment="文章ID")
    title = db.Column(db.String(120), nullable=False, index=True, comment="文章标题")
    content = db.Column(db.Text, comment="文章内容")
    published = db.Column(
        db.Boolean, default=False, nullable=False, index=True, comment="是否已发布"
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, comment="作者ID"
    )

    def __repr__(self) -> str:
        """模型的字符串表示。"""
        return f"<Post(id={self.id}, title='{self.title}', user_id={self.user_id})>"

    def to_dict(self) -> dict:
        """转换为字典格式。

        Returns:
            包含文章基本信息的字典
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "published": self.published,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def publish(self) -> None:
        """发布文章。"""
        self.published = True

    def unpublish(self) -> None:
        """取消发布文章。"""
        self.published = False
