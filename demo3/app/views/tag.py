"""Demo3 标签管理视图模块。

提供标签相关的 CRUD 接口。
"""

from flask import Blueprint, request

from app.extensions import db
from app.models import Tag
from app.schemas import tag_schema, tags_schema
from app.utils import apply_filter, apply_sort, get_page_params, to_pagination_dict
from app.responses import success, created, no_content
from app.errors import NotFoundError, DuplicateError, ValidationErrorAPI

bp = Blueprint("tag", __name__, url_prefix="/api/tags")


@bp.get("")
def list_tags():
    """获取标签列表。

    查询参数:
        page: 页码，默认 1
        per_page: 每页条数，默认 10，最大 100
        name: 按名称筛选（模糊匹配）
        sort: 排序字段（name, created_at, updated_at）
        order: 排序方向（asc, desc）

    Returns:
        标签列表和分页信息
    """
    query = db.session.query(Tag)
    params = request.args.to_dict()

    query = apply_filter(
        query,
        Tag,
        allowed_cols={
            "name": ("name", "contains"),
        },
        params=params,
    )
    query = apply_sort(
        query,
        Tag,
        allowed_cols={"name", "created_at", "updated_at"},
        default_col="created_at",
        default_dir="desc",
        params=params,
    )
    pager = get_page_params(params=params)
    pagination = query.paginate(error_out=False, **pager)

    return success(
        {
            "list": tags_schema.dump(pagination.items),
            "pagination": to_pagination_dict(pagination),
        }
    )


@bp.post("")
def create_tag():
    """创建新标签。

    请求体:
        {
            "name": "标签名称（必填，1-50字符）"
        }

    Returns:
        201: 创建成功
        409: 标签名称已存在
    """
    data = tag_schema.load(request.json)

    # 检查标签名是否已存在
    existing = db.session.query(Tag).filter_by(name=data["name"]).first()
    if existing:
        raise DuplicateError("标签名称")

    try:
        tag = Tag(**data)
        db.session.add(tag)
        db.session.commit()
        return created(tag_schema.dump(tag))
    except Exception as e:
        db.session.rollback()
        raise


@bp.get("/<int:id>")
def get_tag(id: int):
    """获取标签详情。

    Args:
        id: 标签 ID
    """
    tag = db.session.get(Tag, id)
    if not tag:
        raise NotFoundError("标签")
    return success(tag_schema.dump(tag))


@bp.put("/<int:id>")
def update_tag(id: int):
    """更新标签。

    Args:
        id: 标签 ID

    请求体:
        {
            "name": "新标签名称（必填）"
        }
    """
    tag = db.session.get(Tag, id)
    if not tag:
        raise NotFoundError("标签")

    data = tag_schema.load(request.json, partial=True)

    # 检查是否提供了 name
    if "name" not in data:
        raise ValidationErrorAPI("标签名称不能为空")

    # 检查新名称是否与其他标签冲突
    if data["name"] != tag.name:
        existing = (
            db.session.query(Tag).filter(Tag.name == data["name"], Tag.id != id).first()
        )
        if existing:
            raise DuplicateError("标签名称")
        tag.name = data["name"]

    try:
        db.session.commit()
        return success(tag_schema.dump(tag), message="标签更新成功")
    except Exception as e:
        db.session.rollback()
        raise


@bp.delete("/<int:id>")
def delete_tag(id: int):
    """删除标签。

    Args:
        id: 标签 ID
    """
    tag = db.session.get(Tag, id)
    if not tag:
        raise NotFoundError("标签")

    try:
        db.session.delete(tag)
        db.session.commit()
        return no_content()
    except Exception as e:
        db.session.rollback()
        raise
