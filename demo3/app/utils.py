from flask import request
from typing import Dict, Tuple, Literal
from sqlalchemy import asc, desc, or_


def get_page_params(max_per_page=100, default_per_page=10, params=None):
    """
    从查询参数中提取统一的分页信息。

    :param max_per_page: 每页上限，默认 100
    :param default_per_page: 默认每页数量，默认 10
    :return: {"page": int, "per_page": int}
    """
    if params is None:
        params = request.args

    try:
        page = int(params.get("page", 1))
        per_page = int(params.get("per_page", default_per_page))
    except (ValueError, TypeError):
        page = 1
        per_page = default_per_page

    # 合法范围校验
    page = max(1, page)
    per_page = max(1, min(per_page, max_per_page))

    return {"page": page, "per_page": per_page}


def to_pagination_dict(pagination):
    """
    仅把 SQLAlchemy Pagination 对象的分页元信息转成 dict，
    不包含任何 list/records 数据。
    """
    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "has_prev": pagination.has_prev,
        "has_next": pagination.has_next,
    }


# 类型别名：只接受 (字段, 操作符) 元组，操作符固定可选值
OpSpec = Tuple[str, Literal["exact", "contains", "gt", "gte", "lt", "lte"]]


def apply_filter(
    query,
    model,
    allowed_cols: Dict[str, OpSpec],
    params=None,
):
    """
    仅支持显式 (字段, 操作符) 元组形式的 allowed_cols，彻底告别自动推断。
    示例：
    allowed_cols = {
        "id": ("id", "exact"),
        "keyword": ("username,email", "contains"),
        "username": ("username", "exact"),
        "desc": ("desc", "contains"),
        "age_min": ("age", "gte"),
        "age_max": ("age", "lte"),
    }
    """
    if params is None:
        from flask import request

        params = request.args

    for arg_name, (field_spec, op) in allowed_cols.items():
        value = params.get(arg_name)
        if not value:  # 空串或 None 跳过
            continue

        # 支持逗号分隔多字段 OR 查询
        or_fields = [f.strip() for f in field_spec.split(",")]
        clauses = []
        for f in or_fields:
            col = getattr(model, f)
            if op == "exact":
                clauses.append(col == value)
            elif op == "contains":
                clauses.append(col.contains(value))
            elif op == "gt":
                clauses.append(col > value)
            elif op == "gte":
                clauses.append(col >= value)
            elif op == "lt":
                clauses.append(col < value)
            elif op == "lte":
                clauses.append(col <= value)
            else:
                raise ValueError(f"Unsupported operator: {op}")
        query = query.filter(or_(*clauses))

    return query


def apply_sort(
    query, model, allowed_cols, default_col="id", default_dir="asc", params=None
):
    """
    通用排序函数：只操作 query，不依赖 flask request。

    :param query:        SQLAlchemy Query 对象
    :param model:        映射的 ORM 类（如 User）
    :param allowed_cols: set / list  允许排序的字段名
    :param default_col:  默认排序字段（ORM 属性名）
    :param default_dir:  默认方向  'asc' | 'desc'
    :param params:       外部已经解析好的 dict，若空则内部自己读 request.args
    :return:             新的 Query 对象（链式调用）
    """
    if params is None:  # 允许手动注入参数，方便单元测试
        params = request.args

    sort_field = (params.get("sort") or default_col).strip()
    sort_dir = (params.get("order") or default_dir).lower()

    # 合法列用外部传入，否则回退默认
    col_name = sort_field if sort_field in allowed_cols else default_col
    col = getattr(model, col_name)
    return query.order_by(desc(col) if sort_dir == "desc" else asc(col))
