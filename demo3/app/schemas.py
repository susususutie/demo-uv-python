"""Demo3 序列化模式模块。

使用 Marshmallow 进行数据序列化和反序列化，以及请求数据验证。
"""

from marshmallow import Schema, fields, validate


class TagSchema(Schema):
    """标签序列化模式。

    Attributes:
        id: 标签 ID（只读）
        name: 标签名称（必填，1-50 字符）
        created_at: 创建时间（只读）
        updated_at: 更新时间（只读）
    """

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


# 标签模式单例
tag_schema = TagSchema()
tags_schema = TagSchema(many=True)


class UserSchema(Schema):
    """用户序列化模式。

    Attributes:
        id: 用户 ID（只读）
        username: 用户名（必填，2-80 字符）
        email: 邮箱地址（必填，需符合邮箱格式）
        created_at: 创建时间（只读）
        article_count: 文章数量（只读，默认 0）
    """

    id = fields.Int(dump_only=True)
    username = fields.Str(
        required=True,
        validate=[
            validate.Length(min=2, max=80, error="用户名长度必须在 2-80 字符之间"),
            validate.Regexp(
                r"^[\w-]+$", error="用户名只能包含字母、数字、下划线和连字符"
            ),
        ],
    )
    email = fields.Email(required=True, error_messages={"invalid": "无效的邮箱格式"})
    created_at = fields.DateTime(dump_only=True)
    article_count = fields.Int(dump_only=True, dump_default=0)


# 用户模式单例
user_schema = UserSchema()
users_schema = UserSchema(many=True)


class PostSchema(Schema):
    """文章序列化模式。

    Attributes:
        id: 文章 ID（只读）
        title: 文章标题（必填，1-120 字符）
        content: 文章内容（可选）
        published: 是否已发布（默认 False）
        created_at: 创建时间（只读）
        updated_at: 更新时间（只读）
        user_id: 作者 ID（必填）
    """

    id = fields.Int(dump_only=True)
    title = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=120, error="标题长度必须在 1-120 字符之间"),
    )
    content = fields.Str(allow_none=True, load_default="")
    published = fields.Bool(load_default=False, dump_default=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(
        required=True, validate=validate.Range(min=1, error="用户ID必须大于 0")
    )


# 文章模式单例
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class PaginationSchema(Schema):
    """分页信息序列化模式。

    用于统一分页响应的格式。
    """

    page = fields.Int()
    per_page = fields.Int()
    total = fields.Int()
    pages = fields.Int()
    has_prev = fields.Bool()
    has_next = fields.Bool()


# 分页模式单例
pagination_schema = PaginationSchema()
