from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=2, max=80))
    email = fields.Email(required=True)
    created_at = fields.DateTime(dump_only=True)


# 单例供视图直接调用
user_schema = UserSchema()


class PostSchema(Schema):
    id = fields.Int(dump_only=True)  # 只读
    title = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    content = fields.Str()
    published = fields.Bool(load_default=False, dump_default=False)  # 默认 False
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    # data_key="userId" 表示前端传来json的 key 名为 userId，同时在返回json中也使用 userId
    user_id = fields.Int(required=True, dump_only=True)


# 单例
post_schema = PostSchema()
posts_schema = PostSchema(many=True)
